#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# /*******************************************************
#  * Copyright (C) 2013-2014 CloudRunner.io <info@cloudrunner.io>
#  *
#  * Proprietary and confidential
#  * This file is part of CloudRunner Server.
#  *
#  * CloudRunner Server can not be copied and/or distributed
#  * without the express permission of CloudRunner.io
#  *******************************************************/

from __future__ import print_function
import aerospike
import aerospike.predicates as p
from contextlib import contextmanager
import logging
import os

from cloudrunner import CONFIG_LOCATION
from cloudrunner.util.config import Config
from cloudrunner_server.util import timestamp, MAX_TS

CR_CONFIG = Config(CONFIG_LOCATION)
as_host, as_port = CR_CONFIG.AS_URL or '127.0.0.1', CR_CONFIG.AS_PORT or 3000

config = {
    'hosts': [
        (as_host, int(as_port))
    ],
    'lua': {
        'user_path': os.path.join(os.path.dirname(__file__), "functions")
    },
    'policies': {
        'timeout': 1000,  # milliseconds
        'retry': 2,
    }
}

client = aerospike.client(config)
client.connect()
LOG = logging.getLogger('AERO CACHE')
DAYS30 = 30 * 24 * 60 * 60
DAYS7 = 7 * 24 * 60 * 60

LOGS_SET = 'logs'
AUTH_SET = 'auth'
TS_SET = 'timestamps'
MAX_LOG_LINES = 200
MAX_SCORE = MAX_TS * 1000

LOG.info("AEROSPIKE CONFIG: %s" % config)

STR_INDICES = ['owner', 'node', 'uuid']
NUM_INDICES = ['id', 'ts']
AUTH_INDICES = ['token', 'username']


class AeroRegistry(object):

    def __init__(self, **kwargs):
        self.client = client

    def check(self, org, target):
        LOG.info(RegBase.key(TS_SET, org, target))
        try:
            key, meta, last = self.client.get(
                RegBase.key(TS_SET, org, target))
            LOG.info(last)
            if last:
                return last.get('ts', 0)
        except Exception, ex:
            LOG.error(ex)
        return 0

    def associate(self, org, tag, *ids):
        pass
        # client.get((TS_SET, org, target))

    def prepare_space(self, org):
        policy = {}
        ns = LOGS_SET
        _set = org

        for bin in STR_INDICES:
            index_name = "%s-%s" % (_set, bin)
            self.client.index_string_create(policy, ns, _set, bin, index_name)
        for bin in NUM_INDICES:
            index_name = "%s-%s" % (_set, bin)
            self.client.index_integer_create(policy, ns, _set, bin, index_name)

        # Auth
        for bin in AUTH_INDICES:
            index_name = "auth-%s" % bin
            self.client.index_string_create(
                policy, "auth", "tokens", bin, index_name)

    @contextmanager
    def writer(self, org, _id):
        try:
            yield RegWriter(self.client, org, _id)
        except Exception, ex:
            LOG.exception(ex)
            # Do not execute on error
        finally:
            pass

    @contextmanager
    def reader(self, org):
        try:
            yield RegReader(self.client, org)
        except Exception, ex:
            # Do not execute on error
            LOG.exception(ex)
        finally:
            pass


class RegBase(object):

    def __init__(self, client, org, _id):
        self.org = org
        self.id = str(_id)

        self.client = client

    @classmethod
    def key(cls, *args):
        return tuple([str(a) for a in args])


class RegWriter(RegBase):

    def store_log(self, node, ts, log, user, io='O', ttl=None):
        if not log:
            return

        lines = []
        for l in log.splitlines():
            l = l.strip()
            if l:
                lines.append(l)

        inc_ops = [
            {
                "op": aerospike.OPERATOR_INCR,
                "bin": "autoid",
                "val": 1
            },
            {
                "op": aerospike.OPERATOR_READ,
                "bin": "autoid"
            }
        ]
        inc_key = self.key(LOGS_SET, "meta", "inc-%s" % self.org)
        try:
            _, _, data = self.client.operate(inc_key, inc_ops)
        except Exception, (ecode, emsg, efile, eline):
            if ecode == 2:
                self.client.put(inc_key, dict(autoid=0L, org=self.org))
            # retry ...
            _, _, data = self.client.operate(inc_key, inc_ops)

        inc = int(data['autoid'])

        ts = int(ts * 1000)
        key = self.key(LOGS_SET, self.org, "%s-%s" % (self.id, ts))
        rec = dict(id=inc, uuid=self.id, ts=ts, lines=lines,
                   io=io, node=str(node), owner=str(user), type='O')
        ttl = {'ttl': ttl or DAYS30}
        self.client.put(key, rec, ttl)

    def store_meta(self, result, ts, ttl=None):
        key = self.key(LOGS_SET, self.org, self.id)
        ttl = {'ttl': ttl or DAYS30}
        self.client.put(key, dict(type='M',
                                  uuid=self.id,
                                  result=result),
                        ttl)

    def add_token(self, username, token, expire):
        ttl = {'ttl': expire * 60}
        token['username'] = username
        key = self.key(AUTH_SET, "tokens", token['token'])
        self.client.put(key, token, ttl)

    def incr(self, org, what):
        self.client.put(
            self.key(TS_SET, org, what), dict(ts=int(timestamp() * 1000)))


class RegReader(RegBase):

    def __init__(self, client, org):
        self.client = client
        self.org = str(org)
        self.body_filter = None
        self.nodes_filter = None

    def get_user_token(self, user, token):
        key = self.key(AUTH_SET, "tokens", token)
        _, _, val = self.client.get(key)
        if not val:
            return None
        return val

    def get_uuid_by_score(self, min_score=0, max_score=MAX_SCORE):
        q = self.client.query(LOGS_SET, self.org)
        q.select('uuid', 'ts')
        q.where(p.between('ts', int(min_score), int(max_score)))

        lines = set()

        def callback((k, m, rec)):
            if rec.get('ts'):
                lines.add((rec['uuid'], rec['ts']))

            # if len(lines) > MAX_LOG_LINES:
            #     return False

        q.foreach(callback)
        lines = sorted(lines, key=lambda l: l[1])
        ret = zip(*lines)

        if ret:
            return ret[1][-1], ret[0]
        else:
            return 0, []

    def load_log(self, min_score=None, max_score=None, uuids=None, tail=None):
        if not uuids:
            return 0, {}

        output = {'new_score': 1}
        min_score = min_score or 0
        max_score = max_score or int(MAX_SCORE)

        for uuid in uuids:
            q = self.client.query(LOGS_SET, self.org)

            q.where(p.equals('uuid', uuid))

            q.apply('filters', 'score', [min_score, max_score,
                                         self.body_filter, self.nodes_filter])
            data = {}

            def callback(rec):
                if "ts" in rec:
                    output['new_score'] = max(output['new_score'], rec['ts'])
                if rec['type'] == 'O':
                    ts = rec['ts'] / 1000.0
                    data.setdefault(rec['node'],
                                    {}).setdefault('lines',
                                                   []).append([ts,
                                                               rec['lines'],
                                                               rec['io']])
                elif rec['type'] == 'M':
                    for node in rec.get('nodes', []):
                        data.setdefault(node, {})['result'] = rec['result']

            q.foreach(callback)
            for node in data:
                lines = data[node].get("lines", [])
                if lines:
                    data[node]['lines'] = sorted(lines, key=lambda l: l[0])
            output[uuid] = data

        new_score = output.pop('new_score', 1)
        return new_score, output

    def apply_filters(self, pattern=None, nodes=None, **kwargs):
        self.body_filter = pattern
        self.nodes_filter = nodes

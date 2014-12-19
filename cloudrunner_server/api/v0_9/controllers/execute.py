import logging
from pecan import expose, request, abort
from pecan.hooks import HookController

from cloudrunner_server.api.hooks.db_hook import DbHook
from cloudrunner_server.api.util import JsonOutput as O
from cloudrunner_server.api.model import (Revision, Script, Repository,
                                          Folder, ApiKey)
from cloudrunner_server.triggers.manager import TriggerManager

LOG = logging.getLogger()

MAN = TriggerManager()


class Execute(HookController):

    __hooks__ = [DbHook()]

    @expose('json')
    def workflow(self, *args, **kwargs):
        full_path = "/" + "/".join(args)
        LOG.info("Received execute request [%s] from: %s" % (
            full_path, request.client_addr))

        if not getattr(request, "user", None):
            key = kwargs.pop('key')
            if not key:
                return O.error(msg="Missing auth key")

            api_key = request.db.query(ApiKey).filter(
                ApiKey.value == key).first()
            if not api_key:
                return abort(401)
            user_id = api_key.user_id
        else:
            user_id = request.user.id

        version = kwargs.pop("rev", None)
        repo, _dir, scr_name, rev = Script.parse(full_path)

        repo = request.db.query(Repository).filter(
            Repository.name == repo).first()
        if not repo:
            return O.error(msg="Repository '%s' not found" % repo)

        scr = request.db.query(Script).join(Folder).filter(
            Script.name == scr_name, Folder.repository_id == repo.id,
            Folder.full_name == _dir).first()
        if not scr:
            return O.error(msg="Script '%s' not found" % full_path)
        rev = scr.contents(request, rev=version)
        if not rev:
            if version:
                return O.error(msg="Version %s of script '%s' not found" %
                               (version, full_path))
            else:
                return O.error(msg="Script contents for '%s' not found" %
                               full_path)

        request.db.commit()
        task_ids = MAN.execute(user_id=user_id,
                               content=rev,
                               db=request.db,
                               **kwargs)
        return O.success(msg="Dispatched", **task_ids)

    batch = workflow

    @expose('json')
    def script(self, *args, **kwargs):
        full_path = "/" + "/".join(args)
        LOG.info("Received execute request [%s] from: %s" % (
            full_path, request.client_addr))

        targets = kwargs.pop('targets')
        if not getattr(request, "user", None):
            key = kwargs.pop('key')
            if not key:
                return O.error(msg="Missing auth key")

            api_key = request.db.query(ApiKey).filter(
                ApiKey.value == key).first()
            if not api_key:
                return abort(401)
            user_id = api_key.user_id
        else:
            user_id = request.user.id

        version = kwargs.pop("rev", None)
        repo, _dir, scr_name, rev = Script.parse(full_path)

        repo = request.db.query(Repository).filter(
            Repository.name == repo).first()
        if not repo:
            return O.error(msg="Repository '%s' not found" % repo)

        scr = request.db.query(Script).join(Folder).filter(
            Script.name == scr_name, Folder.repository_id == repo.id,
            Folder.full_name == _dir).first()
        if not scr:
            return O.error(msg="Script '%s' not found" % full_path)
        rev = scr.contents(request, rev=version)
        if not rev:
            if version:
                return O.error(msg="Version %s of script '%s' not found" %
                               (version, full_path))
            else:
                return O.error(msg="Script contents for '%s' not found" %
                               full_path)

        scr_text = rev.content
        if not scr_text:
            return O.error(msg="Empty script body")

        request.db.commit()
        task_ids = MAN.execute(user_id=user_id,
                               content=rev,
                               targets=targets,
                               db=request.db,
                               **kwargs)
        return O.success(msg="Dispatched", **task_ids)
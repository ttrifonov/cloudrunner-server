from os import path as p


def install():
    print "Installing CloudRunner OpenStack Plugin"
    from cloudrunner import CONFIG_NODE_LOCATION
    from cloudrunner.util.config import Config

    print "Found node config in %s" % CONFIG_NODE_LOCATION

    config = Config(CONFIG_NODE_LOCATION)
    _path = p.abspath(p.join(p.dirname(__file__), '..', 'transport'))

    config.update('General', 'transport',
                  'cloudrunner_server.plugins.transport.zmq_node_transport.NodeTransport')
    config.update('Plugins', 'node_config',
                  'cloudrunner_server.plugins.config.openstack_ssl_config')
    config.reload()

    print "Cloudrunner node configuration completed"

if __name__ == '__main__':
    install()

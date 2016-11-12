__author__ = 'rakesh.varma'
__author__ = 'rakesh.varma'
from fabric.api import *

class salt_master:

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def remote_command(self, cmd):
        output = sudo(cmd)
        return str(output)

    def ping(self):
        return self.remote_command('python -c "{0};{1}"'.format("import salt.client","print salt.client.LocalClient().cmd('*','test.ping')"))

    def install(self):
        with settings(warn_only = True):
            sudo('add-apt-repository -y ppa:saltstack/salt')
            sudo('apt-get update')
            sudo('apt-get install -y salt-master')
            sudo('service --status-all 2>&1 | grep salt')
            sudo('salt-key -L')

    def keys_accept(self):
        sudo('salt-key -L')
        sudo('salt-key -y --accept-all')

class salt_minion:

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def remote_command(self, cmd):
        output = sudo(cmd)
        return str(output)

    def install(self, master, minion):
        with settings(warn_only = True):
            sudo('add-apt-repository -y ppa:saltstack/salt')
            sudo('apt-get update')
            sudo('apt-get install -y salt-minion')
            cmd = 'echo "master: {0}" > /etc/salt/minion'.format(master)
            sudo(cmd)
            sudo('echo "id: {0}" >> /etc/salt/minion'.format(minion))
            sudo('service --status-all 2>&1 | grep salt')
            sudo('service salt-minion restart')





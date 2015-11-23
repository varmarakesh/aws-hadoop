__author__ = 'rakesh.varma'
from fabric.api import *
class fabric_helper:

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file

    def run_remote_command(self, cmd):
        output = sudo(cmd)
        return str(output)

    def run_salt_master_ping(self):
        return self.run_remote_command('python -c "{0};{1}"'.format("import salt.client","print salt.client.LocalClient().cmd('*','test.ping')"))


    def install_salt_master(self):
        sudo('add-apt-repository -y ppa:saltstack/salt')
        sudo('apt-get update')
        sudo('apt-get install -y salt-master')
        sudo('service --status-all 2>&1 | grep salt')
        sudo('salt-key -L')


    def install_salt_minion(master, minion):
        sudo('add-apt-repository -y ppa:saltstack/salt')
        sudo('apt-get update')
        sudo('apt-get install -y salt-minion')
        cmd = 'echo "master: {0}" > /etc/salt/minion'.format(master)
        sudo(cmd)
        sudo('echo "id: {0}" >> /etc/salt/minion'.format(minion))
        sudo('service --status-all 2>&1 | grep salt')
        sudo('service salt-minion restart')

    def salt_master_keys_accept(self):
        sudo('salt-key -L')
        sudo('salt-key -y --accept-all')




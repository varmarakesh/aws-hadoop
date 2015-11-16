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
__author__ = 'rakesh.varma'
from fabric.api import *

def remote_host_command_output(host_ip, host_user, host_key_file):
    env.host_string = host_ip
    env.user = host_user
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"

    output = run('hostname -i')
    return str(output)
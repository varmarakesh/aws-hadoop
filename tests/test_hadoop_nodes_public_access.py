import unittest
import sys
sys.path.append('../')
from ConfigParser import SafeConfigParser
from fabric_helper import *
import ast

class test_hadoop_nodes_public_access(unittest.TestCase):
    config = SafeConfigParser()
    host_user = None
    host_key_file = None

    def setUp(self):
        self.config.read('aws_hadoop.hosts')
        self.host_user = 'ubuntu'
        self.host_key_file = "~/.ssh/hadoopec2cluster.pem"

    def test_hostnames(self):
        main_config = SafeConfigParser()
        main_config.read('config.ini')
        hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
        for host in hosts:
            host_ip = eval(self.config.get("main", host))['ip_address']
            fb = fabric_helper(host_ip = host_ip, host_user = self.host_user, host_key_file = self.host_key_file)
            self.assertEqual(fb.run_remote_command('hostname'), eval(self.config.get("main", host))['dns_name'])
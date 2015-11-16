import unittest
import sys
sys.path.append('../')
from ConfigParser import SafeConfigParser
from fabric_helper import *

class test_salt_install(unittest.TestCase):
    config = SafeConfigParser()
    host_user = None
    host_key_file = None

    def setUp(self):
        self.config.read('aws_hadoop.hosts')
        self.host_user = 'ubuntu'
        self.host_key_file = "~/.ssh/hadoopec2cluster.pem"


    def test_salt_ping(self):
        """Validates are all salt minions are responding to the ping"""
        saltmaster = self.config.get("main", "saltmaster")
        fb = fabric_helper(host_ip = saltmaster, host_user = self.host_user, host_key_file = self.host_key_file)
        salt_output = fb.run_salt_master_ping()
        self.assertTrue(eval(salt_output)['hadoopnamenode'])
        self.assertTrue(eval(salt_output)['hadoopsecondarynamenode'])
        self.assertTrue(eval(salt_output)['hadoopslave1'])
        self.assertTrue(eval(salt_output)['hadoopslave2'])





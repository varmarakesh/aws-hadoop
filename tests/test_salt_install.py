import unittest
import sys
sys.path.append('../')
from config_operations import *
from node_operations import *
from fabric_helper import *
import ast

class test_salt_install(unittest.TestCase):

    def setUp(self):
        self.config = ConfigOps()
        self.hadoop_cluster = HadoopCluster()


    def test_salt_ping(self):
        """Validates are all salt minions are responding to the ping"""
        saltmaster = self.hadoop_cluster.getNode("saltmaster").ip_address
        fb = fabric_helper(host_ip = saltmaster, host_user = self.config.aws_user, host_key_file = self.config.aws_key_location)
        salt_output = fb.run_salt_master_ping()
        nodes = self.config.all_hadoop_nodes
        for node in nodes:
            self.assertTrue(eval(salt_output)[node])




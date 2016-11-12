import sys
sys.path.append('../')
import unittest
#from config_operations import *
from node_operations import *
from fabric_helper import *
import requests

class integration_tests(unittest.TestCase):

    def setUp(self):
        self.hadoop_cluster = HadoopCluster()

    def test_hadoop_admin(self):
        url = "http://{0}:{1}".format(self.hadoop_cluster.getNode("hadoopnamenode").ip_address, '50070')
        print url
        r = requests.get(url = url)

        self.assertEqual(r.status_code, 200)
__author__ = 'rakesh.varma'
import unittest
from config_operations import *

class test(unittest.TestCase):

    def setUp(self):
        config_path = '../config.ini'
        self.c = ConfigOps(filepath = config_path)
        from hadoop_ops import hadoop
        self.h = hadoop(namenode = self.c.hadoop_namenode, secondaryNamenode = self.c.hadoop_secondary_namenode, dataNodes = self.c.hadoop_slaves)

    def test_hadoop_config_load(self):
        print self.h.core_site_text
        self.assertIsNotNone(self.h.core_site_text)
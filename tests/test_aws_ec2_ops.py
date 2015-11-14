import unittest
import sys
sys.path.append('../')
from aws_ec2_operations import *
from ConfigParser import SafeConfigParser

class test_aws_ec2_ops(unittest.TestCase):
    ec2 = None

    def setUp(self):
        config = SafeConfigParser()
        config.read('config.ini')
        self.ec2 = aws_ec2_operations(config.get('main', 'aws_region'), access_key_id = config.get('main', 'aws_access_key_id'), secret_access_key = config.get('main', 'aws_secret_access_key'))

    def test_ec2_instances(self):
        instances = ['saltmaster', 'hadoopnamenode', 'hadoopsecondarynamenode', 'hadoopslave1', 'hadoopslave2']
        for instance in instances:
            self.assertEqual(instance, self.ec2.getInstance(instance).tags['Name'])

    def test_hadoop_hosts_file(self):
        config = SafeConfigParser()
        config.read('aws_hadoop.hosts')
        instances = ['saltmaster', 'hadoopnamenode', 'hadoopsecondarynamenode', 'hadoopslave1', 'hadoopslave2']

        for instance in instances:
            self.assertEqual(config.get('main', instance), self.ec2.getInstance(instance).ip_address)

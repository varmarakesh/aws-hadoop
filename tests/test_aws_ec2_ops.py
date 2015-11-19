import unittest
import sys
sys.path.append('../')
from aws_ec2_operations import *
from ConfigParser import SafeConfigParser
from fabric_helper import *
import ast

class test_aws_ec2_ops(unittest.TestCase):
    ec2 = None

    def setUp(self):
        config = SafeConfigParser()
        config.read('config.ini')
        self.ec2 = aws_ec2_operations(config.get('main', 'aws_region'), access_key_id = config.get('main', 'aws_access_key_id'), secret_access_key = config.get('main', 'aws_secret_access_key'))
        self.instances = ast.literal_eval(config.get('main','hadoop_nodes'))
        self.instances.append('saltmaster')

    def test_ec2_instances(self):
        """Validating ec2 instances by tag names."""
        for instance in self.instances:
            self.assertEqual(instance, self.ec2.getInstance(instance).tags['Name'])

    def test_hadoop_hosts_file(self):
        """Validating aws_hadoop.hosts file with actual ec2 instance details (public ip address, private ip address and dns name)."""
        config = SafeConfigParser()
        config.read('aws_hadoop.hosts')

        for instance in self.instances:
            instance_details = eval(config.get('main', instance))
            self.assertEqual(instance_details['ip_address'], self.ec2.getInstance(instance).ip_address)
            self.assertEqual(instance_details['private_ip_address'], self.ec2.getInstance(instance).private_ip_address)
            self.assertEqual(instance_details['dns_name'], self.ec2.getInstance(instance).dns_name)
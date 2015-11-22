import unittest
import sys
sys.path.append('../')
from aws_ec2_operations import *
from config_operations import *
from node_operations import *


class test_aws_ec2_ops(unittest.TestCase):
    ec2 = None
    config = ConfigOps()
    instances = []

    def setUp(self):
        self.ec2 = aws_ec2_operations(
            self.config.aws_region,
            access_key_id = self.config.aws_access_key_id,
            secret_access_key = self.config.aws_secret_access_key
        )
        self.instances = self.config.all_nodes

    def test_ec2_instances(self):
        """Validating ec2 instances by tag names."""
        for instance in self.instances:
            self.assertEqual(instance, self.ec2.getInstance(instance).tags['Name'])

    def test_hadoop_hosts_file(self):
        """Validating aws_hadoop.hosts file with actual ec2 instance details (public ip address, private ip address and dns name)."""
        hadoop_nodes = HadoopCluster().nodes

        for node in hadoop_nodes:
            self.assertEqual(node.ip_address, self.ec2.getInstance(node.name).ip_address)
            self.assertEqual(node.private_ip_address, self.ec2.getInstance(node.name).private_ip_address)
            self.assertEqual(node.dns_name, self.ec2.getInstance(node.name).dns_name)

if __name__ == '__main__':
    unittest.main()
__author__ = 'rakesh.varma'
import unittest

class test_python_packages(unittest.TestCase):

    def test_boto_package_exists(self):
        try:
            import boto
            pass
        except:
            self.fail('No boto package found.')

    def test_fabric_package_exists(self):
        try:
            import fabric
            pass
        except:
            self.fail('No fabric package found.')

    def test_paramiko_package_exists(self):
        try:
            import paramiko
            pass
        except:
            self.fail('No paramiko package found.')


    def test_ecdsa_package_exists(self):
        try:
            import ecdsa
            pass
        except:
            self.fail('No ecdsa package found.')

class test_config(unittest.TestCase):

    def setUp(self):
        import sys
        sys.path.append('../')
        import config_operations
        self.c = config_operations.ConfigOps()

    def test_config(self):
        try:
            salt = self.c.saltmaster
            pass
        except:
            self.fail('Config settings failed to load. check config.ini')

    def test_config_hadoop_nodes(self):
        try:
            namenode = self.c.hadoop_namenode
            secondarynamenode = self.c.hadoop_secondary_namenode
            slaves = self.c.hadoop_slaves
            pass
        except:
            self.fail('Exception while reading hadoop nodes from config, there should be atleast one namenode, secondaryname and slave.')

    def test_ec2_connection(self):
        from aws_ec2_operations import aws_ec2_operations
        import boto.ec2
        try:
            ec2 = aws_ec2_operations(region = self.c.aws_region, access_key_id = self.c.aws_access_key_id, secret_access_key = self.c.aws_secret_access_key)
            instances = ec2.ec2.get_only_instances()
            pass
        except boto.exception.EC2ResponseError:
           self.fail('Exception while opening a AWS connection. Please check region, aws_access_key_id and aws_secret_access_key.')


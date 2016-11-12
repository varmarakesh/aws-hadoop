__author__ = 'rakesh.varma'
from aws_ec2_operations import *
from config_operations import *

class hadoop_cluster:
    ec2 = None
    c = None

    def __init__(self):
        self.c = ConfigOps()
        self.ec2 = aws_ec2_operations(
            region = self.c.aws_region,
            access_key_id = self.c.aws_access_key_id,
            secret_access_key = self.c.aws_secret_access_key
        )

    def pre_checks(self):
        from aws_ec2_operations import aws_ec2_operations
        import boto.ec2
        try:
            ec2 = aws_ec2_operations(region = self.c.aws_region, access_key_id = self.c.aws_access_key_id, secret_access_key = self.c.aws_secret_access_key)
            instances = ec2.ec2.get_only_instances()
        except boto.exception.EC2ResponseError:
            raise Exception('Exception while opening a AWS connection. Please check region, aws_access_key_id and aws_secret_access_key.')

        print 'Pre-checks passed'

    def create_instances(self):
        self.ec2.create_instances(
            image_id = self.c.aws_image_id,
            key_name = self.c.aws_key_name,
            instance_type = self.c.aws_instance_type,
            security_group = self.c.aws_security_group,
            instances = self.c.all_nodes
        )

    def post_checks(self):
        from node_operations import *
        hadoop_nodes = HadoopCluster().nodes

        for node in hadoop_nodes:
            check = (node.ip_address == self.ec2.ec2.getInstance(node.name).ip_address) and \
                    (node.private_ip_address == self.ec2.ec2.getInstance(node.name).private_ip_address ) and \
                    (node.dns_name == self.ec2.ec2.getInstance(node.name).dns_name)

            if not check:
                raise Exception('Checks on aws_hadoop.hosts failed.')

        print 'Post-checks passed.'



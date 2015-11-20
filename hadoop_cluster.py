__author__ = 'rakesh.varma'
from aws_ec2_operations import *
from config_operations import *


def main():
    c = ConfigOps()

    ec2 = aws_ec2_operations(
        region=c.aws_region,
        access_key_id=c.aws_access_key_id,
        secret_access_key=c.aws_secret_access_key
    )

    ec2.create_instances(
        image_id=c.aws_image_id,
        key_name=c.aws_key_name,
        instance_type=c.aws_instance_type,
        security_group=c.aws_security_group,
        instances=c.all_nodes
    )

if __name__ == '__main__':
    main()

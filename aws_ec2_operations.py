__author__ = 'rakesh.varma'
import boto.ec2


class aws_ec2_operations:

    ec2 = None

    def __init__(self, region, access_key_id, secret_access_key):
        self.ec2 = boto.ec2.connect_to_region(region, aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)

    def create_instances(self, image_id, key_name, instance_type, security_group, instances):
        reservation = self.ec2.run_instances(
                                                image_id = image_id,
                                                key_name = key_name,
                                                instance_type = instance_type,
                                                security_groups =[security_group],
                                                min_count = len(instances),
                                                max_count = len(instances)
        )

        for i, instance in enumerate(reservation.instances):
            instance.add_tag("Name", instances[i])

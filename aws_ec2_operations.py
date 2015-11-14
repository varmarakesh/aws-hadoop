__author__ = 'rakesh.varma'
import boto.ec2
from ConfigParser import SafeConfigParser
import time

class aws_ec2_operations:

    ec2 = None

    def __init__(self, region, access_key_id, secret_access_key):
        self.ec2 = boto.ec2.connect_to_region(region, aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)

    def getInstance(self, name):
        for instance in self.ec2.get_only_instances():
            if instance.state <> 'terminated':
                if instance.tags['Name'] == name:
                    return instance
        return None

    def create_instances(self, image_id, key_name, instance_type, security_group, instances):
        #create ec2 instances.
        reservation = self.ec2.run_instances(
                                                image_id = image_id,
                                                key_name = key_name,
                                                instance_type = instance_type,
                                                security_groups =[security_group],
                                                min_count = len(instances),
                                                max_count = len(instances)
        )

        time.sleep(10)
        #add tags to the created instances.
        for index, instance in enumerate(reservation.instances):
            instance.add_tag("Name", instances[index])


        time.sleep(10)
        #update the aws_hadoop.hosts file with the instance tag and the public ip address.
        c = SafeConfigParser()
        c.add_section("main")
        hadoop_cfgfile = open("aws_hadoop.hosts", 'w')

        for instance in instances:
            inst = self.getInstance(instance)
            c.set("main",instance, str(inst.ip_address))
        c.write(hadoop_cfgfile)
        hadoop_cfgfile.close()

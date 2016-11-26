__author__ = 'rakesh.varma'
from boto import cloudformation, ec2

class hadoop_cluster:

    instances = []
    def __init__(self, instances):
        self.instances = instances

    @property
    def saltmaster(self):
        return [instance.dns_name for instance in self.instances if instance.tags['Name'] == 'saltmaster'][0]

    @property
    def namenode(self):
        return [instance.dns_name for instance in self.instances if instance.tags['Name'] == 'namenode'][0]

    @property
    def secondarynamenode(self):
        return [instance.dns_name for instance in self.instances if instance.tags['Name'] == 'secondarynamenode'][0]

    @property
    def datanodes(self):
        return [instance.dns_name for instance in self.instances if instance.tags['Name'].find('datanode') <> -1]

    @property
    def all_hadoop_nodes(self):
        nodes = []
        nodes.append(self.namenode)
        nodes.append(self.secondarynamenode)
        for slave in self.datanodes:
            nodes.append(slave)
        return nodes

    @property
    def all_nodes(self):
        nodes = self.all_hadoop_nodes
        nodes.append(self.saltmaster)
        return nodes

class cf:

    def __init__(self, aws_access_key_id, aws_secret_access_key, security_token):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.security_token = security_token
        self.cf = cloudformation.connect_to_region(region_name = 'us-west-2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, security_token = security_token)
        self.ec2 = ec2.connect_to_region('us-west-2', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, security_token = security_token)

    def get_instance_by_id(self, id):
        for instance in self.ec2.get_only_instances():
            if instance.id == id:
                return instance

    def get_stack_resources(self, name):
        return [self.get_instance_by_id(resource.physical_resource_id) for resource in self.cf.list_stack_resources(name) if resource.resource_type == 'AWS::EC2::Instance']

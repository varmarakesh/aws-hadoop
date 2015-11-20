__author__ = 'rakesh.varma'
from ConfigParser import *

class ConfigOps:
    def __init__(self):
        self.config = SafeConfigParser()
        self.config.read('config.ini')

    @property
    def hadoop_namenode(self):
        hadoop_nodes =  eval(self.config.get("main", "hadoop_nodes"))
        return hadoop_nodes['namenode']


    @property
    def hadoop_secondary_namenode(self):
        hadoop_nodes =  eval(self.config.get("main", "hadoop_nodes"))
        return hadoop_nodes['secondarynamenode']

    @property
    def hadoop_slaves(self):
        hadoop_nodes =  eval(self.config.get("main", "hadoop_nodes"))
        return list(hadoop_nodes['slaves'])

    @property
    def aws_key_location(self):
        return self.config.get("main", "aws_key_location")

    @property
    def aws_region(self):
        return self.config.get("main", "aws_region")

    @property
    def aws_access_key_id(self):
        return self.config.get("main", "aws_access_key_id")

    @property
    def aws_secret_access_key(self):
        return self.config.get("main", "aws_secret_access_key")

    @property
    def aws_image_id(self):
        return self.config.get("main", "aws_image_id")

    @property
    def aws_key_name(self):
        return self.config.get("main", "aws_key_name")

    @property
    def aws_instance_type(self):
        return self.config.get("main", "aws_instance_type")

    @property
    def aws_security_group(self):
        return self.config.get("main", "aws_security_group")

    @property
    def aws_user(self):
        return self.config.get("main", "aws_user")

    @property
    def all_hadoop_nodes(self):
        nodes = []
        nodes.append(self.hadoop_namenode)
        nodes.append(self.hadoop_secondary_namenode)
        for slave in self.hadoop_slaves:
            nodes.append(slave)
        return nodes

    @property
    def all_nodes(self):
        nodes = self.all_hadoop_nodes
        nodes.append("saltmaster")
        return nodes

__author__ = 'rakesh.varma'
__author__ = 'rakesh.varma'
from ConfigParser import *

class ConfigOps:
    def __init__(self, filepath):
        self.config = SafeConfigParser()
        self.config.read(filepath)

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
    def saltmaster(self):
        return self.config.get("main","salt_master")

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
        nodes.append(self.saltmaster)
        return nodes

    @property
    def key_location(self):
        return self.config.get("main", "key_location")

    @property
    def user(self):
        return self.config.get("main", "user")


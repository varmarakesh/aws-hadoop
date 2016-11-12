__author__ = 'rakesh.varma'
from ConfigParser import SafeConfigParser
import os

class Node:
    name = None
    ip_address = None
    private_ip_address = None
    dns_name = None

    def __init__(self, name, ip_address, private_ip_address, dns_name):
        self.name = name
        self.ip_address = ip_address
        self.private_ip_address  = private_ip_address
        self.dns_name = dns_name

class HadoopCluster:
    nodes = []

    def __init__(self):
        config = SafeConfigParser()
        file_path = os.path.join(os.path.dirname(__file__), 'aws_hadoop.hosts')
        config.read(file_path)
        for item in config.items("main"):
            name = item[0]
            private_ip_address = eval(item[1])['private_ip_address']
            ip_address = eval(item[1])['ip_address']
            dns_name = eval(item[1])['dns_name']
            node = Node(name = name, private_ip_address = private_ip_address, ip_address = ip_address, dns_name = dns_name)
            self.nodes.append(node)

    def getNode(self, name):
        for node in self.nodes:
            if node.name == name:
                return node






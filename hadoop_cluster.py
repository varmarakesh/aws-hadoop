__author__ = 'rakesh.varma'
from aws_ec2_operations import *
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

region = config.get('main', 'aws_region')
access_key_id = config.get('main', 'aws_access_key_id')
secret_access_key = config.get('main', 'aws_secret_access_key')
image_id = config.get('main', 'aws_image_id')
key_name = config.get('main', 'aws_key_name')
instance_type = config.get('main', 'aws_instance_type')
security_group = config.get('main', 'aws_security_group')


ec2 = aws_ec2_operations(region = region, access_key_id = access_key_id, secret_access_key  = secret_access_key)
ec2.create_instances(image_id = image_id, key_name = key_name, instance_type = instance_type, security_group = security_group , instances = ['saltmaster', 'hadoopnamenode', 'hadoopsecondarynamenode', 'hadoopslave1', 'hadoopslave2'])

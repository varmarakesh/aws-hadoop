__author__ = 'rakesh.varma'
from fabric import *
from fabric.api import *
from aws_ec2_operations import *

@task
def local_create_hadoop_cluster():
    #ec2 = aws_ec2_operations(region = 'us-west-2', access_key_id = 'AKIAIAWIUPFHWRWHEN4Q', secret_access_key  = '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')
    #ec2.create_instances(image_id = 'ami-5189a661', key_name = 'hadoopcluster', instance_type = 't2.micro', security_group = 'HadoopEC2SecurityGroup' , instances = ['saltmaster', 'hadoopnamenode', 'hadoopsecondarynamenode', 'hadoopslave1', 'hadoopslave2']])
    local('python hadoop_cluster.py')

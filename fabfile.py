__author__ = 'rakesh.varma'
from fabric import *
from fabric.api import *
from aws_ec2_operations import *

@task
def local_create_hadoop_cluster():
    local('python hadoop_cluster.py')

@task
def local_test_hadoop_cluster():
    local('python -m unittest -v tests.test_aws_ec2_ops')

@task

def local_git_push(msg):
    local('git add .')

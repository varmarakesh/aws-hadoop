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
def git_commit(msg):
    local('git add .')
    local('git commit -m {0}'.format(msg))

@task
def git_commit_push(msg):
    local('git add .')
    local('git commit -m {0}'.format(msg))
    local('git config --global user.email "{0}"'.format('varma.rakesh@gmail.com'))
    local('git config user.name {0}'.format('rakesh varma'))
    local('git remote add origin https://varmarakesh@github.org/varmarakesh/aws-hadoop.git')
    local('git push origin master')
    local('git status')
    local('git log --oneline')



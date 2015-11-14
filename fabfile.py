__author__ = 'rakesh.varma'
from fabric.api import *
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('aws_hadoop.hosts')
#env.user = 'ubuntu'
#env.key_filename = "~/.ssh/hadoopec2cluster.pem"
@task
def create_hadoop_cluster():
    local('python hadoop_cluster.py')

@task
def test_hadoop_cluster():
    local('python -m unittest -v tests.test_aws_ec2_ops')

@task
def git_commit(msg):
    local('git config --global user.email "{0}"'.format('varma.rakesh@gmail.com'))
    local('git config --global user.name "{0}"'.format('varma.rakesh'))
    local('git add .')
    local('git commit -m {0}'.format(msg))

@task
def git_commit_push(msg):
    local('git config --global user.email "{0}"'.format('varma.rakesh@gmail.com'))
    local('git config --global user.name "{0}"'.format('varma.rakesh'))
    local('git add .')
    #local('git rm --cached config.ini')
    local('git commit -m "{0}"'.format(msg))
    local('git remote set-url origin git@github.com:varmarakesh/aws-hadoop.git')
    local('git push origin master')
    local('git status')
    local('git log --oneline')

@task
def salt_master_install():
    env.host_string = config.get("main", "saltmaster")
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('add-apt-repository -y ppa:saltstack/salt')
    sudo('apt-get update')
    sudo('apt-get install -y salt-master')
    sudo('service --status-all 2>&1 | grep salt')
    sudo('salt-key -L')

@task
def salt_minion_install():
    hosts = ['hadoopnamenode','hadoopsecondarynamenode', 'hadoopslave1', 'hadoopslave2']
    for host in hosts:
        env.host_string = config.get('main', host)
        env.user = 'ubuntu'
        env.key_filename = "~/.ssh/hadoopec2cluster.pem"
        sudo('add-apt-repository -y ppa:saltstack/salt')
        sudo('apt-get update')
        sudo('apt-get install -y salt-minion')
        sudo('echo "master:{0} > /etc/salt/minion"'.format(config.get('main', 'saltmaster')))
        sudo('echo "id:{0} >> /etc/salt/minion"'.format(host))
        sudo('service --status-all 2>&1 | grep salt')
        sudo('service salt-minion restart')

@task
def salt_master_keys_accept():
    env.host_string = config.get("main", "saltmaster")
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt-key -L')
    sudo('salt-key -y --accept-all')

def remote_test():
    env.host_string = '52.33.114.9'
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"

    output = run('hostname -i')['<local-only>']
    return output
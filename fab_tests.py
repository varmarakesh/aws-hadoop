from fabric.api import *
from config_operations import *
from node_operations import *
from fabric_helper import *

c = ConfigOps()
hadoop_cluster = HadoopCluster()


@task
def test_hadoop_cluster():
    local('python -m unittest -v tests.test_aws_ec2_ops')

@task
def test_salt():
    local('python -m unittest -v tests.test_salt_install')

@task
def test_hadoop_nodes_public_access():
    local('python -m unittest -v tests.test_hadoop_nodes_public_access')

@task
def test_environment():
    local('python -m unittest -v tests.test_environment')

@task
def test_java():
    env.host_string = hadoop_cluster.getNode(c.saltmaster).ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt "*" cmd.run "java -version"')

@task
def clean_install_hadoop():
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt "*" cmd.run "rm -rf /home/ubuntu/hadoop"')
    sudo('salt "*" cmd.run "rm -f /home/ubuntu/hadoop-2.7.1.tar.gz"')
    sudo('salt "*" cmd.run "wget http://apache.mirror.gtcomm.net/hadoop/common/current/hadoop-2.7.1.tar.gz -P /home/ubuntu"')
    sudo('salt "*" cmd.run "tar -xzvf /home/ubuntu/hadoop-2.7.1.tar.gz -C /home/ubuntu"')
    sudo('salt "*" cmd.run "mv /home/ubuntu/hadoop-2.7.1 /home/ubuntu/hadoop"')

@task
def test_hadoop():
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt "*" cmd.run "ls -lt /home/ubuntu/hadoop"')
    sudo('salt "*" cmd.run "ls -lt /usr/lib/jvm/java-7-oracle"')
    sudo('salt "*" cmd.run "echo $HADOOP_CONF"')
    sudo('salt "*" cmd.run "echo $HADOOP_PREFIX"')

@task
def test_hadoop_master_slave_setup():
    with settings(warn_only = True):
        env.host_string = hadoop_cluster.getNode(c.saltmaster).ip_address
        env.user = c.aws_user
        env.key_filename = c.aws_key_location
        sudo("salt '*' cmd.run 'cat /home/ubuntu/hadoop/etc/hadoop/masters'")
        sudo("salt '*' cmd.run 'cat /home/ubuntu/hadoop/etc/hadoop/slaves'")
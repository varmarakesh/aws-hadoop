from fabric.api import *
from fabric.api import env, put, run, sudo, task, cd, settings, prefix, shell_env
from fabric_ops import fabric_ops
from salt import salt_master, salt_minion
from hadoop_ops import hadoop
from cloudFormationOps import *
import time



@task
def keys(aws_access_key_id, aws_secret_access_key, aws_key_location, cloud_formation_stack, aws_security_token = None):
    c = cf(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, security_token = aws_security_token)
    instances =  c.get_stack_resources(cloud_formation_stack)
    env.cluster = hadoop_cluster(instances = instances)
    env.h = hadoop(namenode = env.cluster.namenode, secondaryNamenode = env.cluster.secondarynamenode, dataNodes = env.cluster.datanodes)
    env.user = 'ubuntu'
    env.key_location = aws_key_location


@task
def salt_install():
    master = salt_master(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)
    master.install()
    time.sleep(5)
    for node in env.cluster.all_hadoop_nodes:
        minion = salt_minion(host_ip = node, host_user = env.user, host_key_file = env.key_location)
        minion.install(master = env.cluster.saltmaster, minion = node)
        time.sleep(2)

    master = salt_master(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)
    master.keys_accept()
    master.ping()

@task
def grant_access_hadoop_nodes():
    for node in env.cluster.all_hadoop_nodes:
        n = fabric_ops(host_ip = node, host_user = env.user, host_key_file = env.key_location)
        #Changing the host name of hadoop nodes to EC2 public dns name.
        cmd_change_hostname = 'hostname {0}'.format(node)
        sudo(cmd_change_hostname)
        #Changing /etc/hosts file to remove localhost and replacing it with the public dns name and 127.0.0.1 with localip.
        #sudo('sed -i -e "s/localhost/{0}/" /etc/hosts'.format(node))

    n = fabric_ops(host_ip = env.cluster.namenode, host_user = env.user, host_key_file = env.key_location)
    run('ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -N ""')
    #adding StrictHostKeyChecking no in the .ssh/config file so that ssh login is not prompted.
    run('echo "{0}" > /home/ubuntu/.ssh/config'.format("Host *"))
    run('echo "{0}" >> /home/ubuntu/.ssh/config'.format("   StrictHostKeyChecking no"))
    #Getting public key from hadoopnamenode
    public_key = sudo('cat /home/ubuntu/.ssh/id_rsa.pub')
    n = fabric_ops(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)

    #Issuing a minion blast of public key to all hadoop nodes to enable passwordless login.
    minion_cmd = "echo '{0}' >> /home/ubuntu/.ssh/authorized_keys".format(public_key)
    sudo('salt "*" cmd.run "{0}"'.format(minion_cmd))

@task
def install_java():
    n = fabric_ops(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)
    with settings(warn_only = True):
        sudo('salt "*" cmd.run "sudo apt-get update"')
        sudo('salt "*" cmd.run "sudo add-apt-repository ppa:webupd8team/java"')
        sudo('salt "*" cmd.run "echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections"')
        sudo('salt "*" cmd.run "sudo apt-get update"')
        sudo('salt "*" cmd.run "sudo apt-get install -y oracle-java8-installer"')
        sudo('salt "*" cmd.run "sudo apt-get -f -y -q install"')
        cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export JAVA_HOME=/usr/lib/jvm/java-8-oracle")
        sudo('salt "*" cmd.run "{0}"'.format(cmd))

@task
def install_hadoop_packages():
    n = fabric_ops(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)
    mirror_site = "http://www-us.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz"
    #Install hadoop binaries
    with settings(warn_only = True):
        sudo('salt "*" cmd.run "wget {0} -P /home/ubuntu"'.format(mirror_site))
        sudo('salt "*" cmd.run "tar -xzvf /home/ubuntu/hadoop-2.7.3.tar.gz -C /home/ubuntu"')
        sudo('salt "*" cmd.run "mv /home/ubuntu/hadoop-2.7.3 /home/ubuntu/hadoop"')
        sudo('salt "*" cmd.run "rm -rf /home/ubuntu/hadoop-2.7.3.tar.gz"')
        #changing the hadoop directory owner to ubuntu.
        sudo('salt "*" cmd.run "sudo chown -R ubuntu /home/ubuntu/hadoop"')

    #Sets environment variables and adds them to path.
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export HADOOP_CONF=/home/ubuntu/hadoop/etc/hadoop")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export HADOOP_PREFIX=/home/ubuntu/hadoop")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export PATH='$'PATH:'$'HADOOP_PREFIX/bin")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))

@task
def deploy_hadoop_config():
    n = fabric_ops(host_ip = env.cluster.namenode, host_user = env.user, host_key_file = env.key_location)

    hadoop_env_command = "sed -i -e s/'\\\${JAVA_HOME}'/'\\\/usr\\\/lib\\\/jvm\\\/java-8-oracle'/ /home/ubuntu/hadoop/etc/hadoop/hadoop-env.sh"

    n = fabric_ops(host_ip = env.cluster.saltmaster, host_user = env.user, host_key_file = env.key_location)
    sudo('salt "*" cmd.run "{0}"'.format(hadoop_env_command))
    core_site_command = "echo '{0}' > {1}".format(env.h.core_site_text, env.h.config_coresite_path)
    sudo('salt "*" cmd.run "{0}"'.format(core_site_command))
    hdfs_site_command = "echo '{0}' > {1}".format(env.h.hdfs_site_text, env.h.config_hdfssite_path)
    sudo('salt "*" cmd.run "{0}"'.format(hdfs_site_command))
    mapred_site_command = "echo '{0}' > {1}".format(env.h.mapred_site_text, env.h.config_mapredsite_path)
    sudo('salt "*" cmd.run "{0}"'.format(mapred_site_command))

@task
def setup_hadoop_master_slave():
    n = fabric_ops(host_ip = env.cluster.namenode, host_user = env.user, host_key_file = env.key_location)
    sudo("echo {0} > {1}".format(env.cluster.namenode, env.h.config_master_path))
    sudo("echo {0} >> {1}".format(env.cluster.secondarynamenode, env.h.config_master_path))
    sudo(">{0}".format(env.h.config_slave_path))
    for slave in env.cluster.datanodes:
        sudo("echo {0} >> {1}".format(slave, env.h.config_slave_path))

    n = fabric_ops(host_ip = env.cluster.secondarynamenode, host_user = env.user, host_key_file = env.key_location)
    sudo("echo {0} > {1}".format(env.cluster.namenode, env.h.config_master_path))
    sudo("echo {0} >> {1}".format(env.cluster.secondarynamenode, env.h.config_master_path))
    sudo(">{0}".format(env.h.config_slave_path))
    for slave in env.cluster.datanodes:
        sudo("echo {0} >> {1}".format(slave, env.h.config_slave_path))

    for slave in env.cluster.datanodes:
        n = fabric_ops(host_ip = slave, host_user = env.user, host_key_file = env.key_location)
        sudo("echo {0} > {1}".format(slave, env.h.config_slave_path))

@task
def start_services_hadoop_master():
    n = fabric_ops(host_ip = env.cluster.namenode, host_user = env.user, host_key_file = env.key_location)
    run("/home/ubuntu/hadoop/bin/hadoop namenode -format -force")
    run("/home/ubuntu/hadoop/sbin/start-dfs.sh")
    run("jps")

@task
def run_pi_test():
    n = fabric_ops(host_ip = env.cluster.namenode, host_user = env.user, host_key_file = env.key_location)
    with cd('/home/ubuntu/hadoop/share/hadoop/mapreduce'):
        run('/home/ubuntu/hadoop/bin/hadoop jar hadoop-mapreduce-examples-2.7.3.jar pi 10 1000000')


@task
def provision_hadoop_cluster():
    execute(salt_install)
    execute(grant_access_hadoop_nodes)
    execute(install_java)
    execute(install_hadoop_packages)
    execute(deploy_hadoop_config)
    execute(setup_hadoop_master_slave)
    execute(start_services_hadoop_master)
    execute(run_pi_test)


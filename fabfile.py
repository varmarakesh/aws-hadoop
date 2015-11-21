__author__ = 'rakesh.varma'
from fabric.api import *
from ConfigParser import SafeConfigParser
import ast
from config_operations import *
from node_operations import *
import time


host_config = SafeConfigParser()
host_config.read('aws_hadoop.hosts')

main_config = SafeConfigParser()
main_config.read('config.ini')

c = ConfigOps()
hadoop_cluster = HadoopCluster()

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
    time.sleep(10)
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('add-apt-repository -y ppa:saltstack/salt')
    sudo('apt-get update')
    sudo('apt-get install -y salt-master')
    sudo('service --status-all 2>&1 | grep salt')
    sudo('salt-key -L')

@task
def salt_minion_install():

    hosts = c.all_hadoop_nodes
    env.user = c.aws_user
    env.key_filename = c.aws_key_location

    for host in hosts:
        env.host_string = hadoop_cluster.getNode(host).ip_address
        sudo('add-apt-repository -y ppa:saltstack/salt')
        sudo('apt-get update')
        sudo('apt-get install -y salt-minion')
        cmd = 'echo "master: {0}" > /etc/salt/minion'.format(hadoop_cluster.getNode("saltmaster").ip_address)
        sudo(cmd)
        sudo('echo "id: {0}" >> /etc/salt/minion'.format(host))
        sudo('service --status-all 2>&1 | grep salt')
        sudo('service salt-minion restart')

@task
def salt_master_keys_accept():
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt-key -L')
    sudo('salt-key -y --accept-all')

@task
def test_salt():
    local('python -m unittest -v tests.test_salt_install')

@task
def hadoop_nodes_setup_access():
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    hosts = c.all_hadoop_nodes
    for host in hosts:
        env.host_string = hadoop_cluster.getNode(host).ip_address
        #Changing the host name of hadoop nodes to EC2 public dns name.
        cmd_change_hostname = 'hostname {0}'.format(hadoop_cluster.getNode(host).dns_name)
        sudo(cmd_change_hostname)
        #Changing /etc/hosts file to remove localhost and replacing it with the public dns name and 127.0.0.1 with localip.
        sudo('sed -i -e "s/localhost/{0}/" /etc/hosts'.format(hadoop_cluster.getNode(host).dns_name))
        sudo('sed -i -e "s/127.0.0.1/{0}/" /etc/hosts'.format(hadoop_cluster.getNode(host).private_ip_address))


    # Setting up passwordless login from hadoopnamenode to all other hadoop nodes.
    env.host_string = hadoop_cluster.getNode(c.hadoop_namenode).ip_address
    #generating ssh keys in id_rsa, no passphrase.
    run('ssh-keygen -t rsa -f /home/ubuntu/.ssh/id_rsa -q -N ""')
    #Getting public key from hadoopnamenode
    public_key = sudo('cat /home/ubuntu/.ssh/id_rsa.pub')

    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address

    #Issuing a minion blast of public key to all hadoop nodes to enable passwordless login.
    minion_cmd = "echo '{0}' >> /home/ubuntu/.ssh/authorized_keys".format(public_key)
    sudo('salt "*" cmd.run "{0}"'.format(minion_cmd))


@task
def test_hadoop_nodes_public_access():
    local('python -m unittest -v tests.test_hadoop_nodes_public_access')

@task
def hadoop_nodes_jdk_install():
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    with settings(warn_only = True):
        sudo('salt "*" cmd.run "sudo apt-get update"')
        sudo('salt "*" cmd.run "sudo add-apt-repository ppa:webupd8team/java"')
        sudo('salt "*" cmd.run "echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections"')
        sudo('salt "*" cmd.run "sudo apt-get update && sudo apt-get install -y oracle-jdk7-installer"')
        sudo('salt "*" cmd.run "sudo apt-get -f -y -q install"')


@task
def test_java():
    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt "*" cmd.run "java -version"')

@task
def hadoop_install():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt "*" cmd.run "wget http://apache.mirror.gtcomm.net/hadoop/common/current/hadoop-2.7.1.tar.gz -P /home/ubuntu"')
    sudo('salt "*" cmd.run "tar -xzvf /home/ubuntu/hadoop-2.7.1.tar.gz -C /home/ubuntu"')
    sudo('salt "*" cmd.run "mv /home/ubuntu/hadoop-2.7.1 /home/ubuntu/hadoop"')
    sudo('salt "*" cmd.run "rm -rf /home/ubuntu/hadoop-2.7.1.tar.gz"')
    #changing the hadoop directory owner to ubuntu.
    sudo('salt "*" cmd.run "sudo chown -R ubuntu /home/ubuntu/hadoop"')
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export HADOOP_CONF=/home/ubuntu/hadoop/etc/hadoop")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export HADOOP_PREFIX=/home/ubuntu/hadoop")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export JAVA_HOME=/usr/lib/jvm/java-7-oracle")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))
    cmd = "echo '{0}' >> /home/ubuntu/.bashrc".format("export PATH='$'PATH:'$'HADOOP_PREFIX/bin")
    sudo('salt "*" cmd.run "{0}"'.format(cmd))

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
def hadoop_config_deploy():
    hadoopnamenode = hadoop_cluster.getNode(c.hadoop_namenode).dns_name

    hadoop_env_command = "sed -i -e s/'\\\${JAVA_HOME}'/'\\\/usr\\\/lib\\\/jvm\\\/java-7-oracle'/ /home/ubuntu/hadoop/etc/hadoop/hadoop-env.sh"
    core_site_text = """<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>fs.default.name</name>
                        <value>hdfs://{0}:8020</value>
                        </property>
                        <property>
                        <name>hadoop.tmp.dir</name>
                        <value>/home/ubuntu/hdfstmp</value>
                        </property>
                        </configuration>""".format(hadoopnamenode)

    hdfs_site_text = """<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>dfs.replication</name>
                        <value>2</value>
                        </property>
                        <property>
                        <name>dfs.permissions</name>
                        <value>false</value>
                        </property>
                        </configuration>"""
    mapred_site_text ="""<?xml version=\\""1.0\\"" encoding=\\""UTF-8\\""?>
                        <?xml-stylesheet type=\\""text/xsl\\"" href=\\""configuration.xsl\\""?>
                        <configuration>
                        <property>
                        <name>mapred.job.tracker</name>
                        <value>hdfs://{0}:8021</value>
                        </property>
                        </configuration>""".format(hadoopnamenode)


    env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo('salt "*" cmd.run "{0}"'.format(hadoop_env_command))
    core_site_command = "echo '{0}' > /home/ubuntu/hadoop/etc/hadoop/core-site.xml".format(core_site_text)
    sudo('salt "*" cmd.run "{0}"'.format(core_site_command))
    hdfs_site_command = "echo '{0}' > /home/ubuntu/hadoop/etc/hadoop/hdfs-site.xml".format(hdfs_site_text)
    sudo('salt "*" cmd.run "{0}"'.format(hdfs_site_command))
    mapred_site_command = "echo '{0}' > /home/ubuntu/hadoop/etc/hadoop/mapred-site.xml".format(mapred_site_text)
    sudo('salt "*" cmd.run "{0}"'.format(mapred_site_command))

@task
def hadoop_master_slave_setup():
    env.host_string = hadoop_cluster.getNode(c.hadoop_namenode).ip_address
    env.user = c.aws_user
    env.key_filename = c.aws_key_location
    sudo("echo {0} > /home/ubuntu/hadoop/etc/hadoop/masters".format(hadoop_cluster.getNode(c.hadoop_namenode).dns_name))
    sudo("echo {0} >> /home/ubuntu/hadoop/etc/hadoop/masters".format(hadoop_cluster.getNode(c.hadoop_secondary_namenode).dns_name))
    sudo(">/home/ubuntu/hadoop/etc/hadoop/slaves")
    for slave in c.hadoop_slaves:
        sudo("echo {0} >> /home/ubuntu/hadoop/etc/hadoop/slaves".format(hadoop_cluster.getNode(slave).dns_name))

    env.host_string = hadoop_cluster.getNode(c.hadoop_secondary_namenode).ip_address
    sudo("echo {0} > /home/ubuntu/hadoop/etc/hadoop/masters".format(hadoop_cluster.getNode(c.hadoop_namenode).dns_name))
    sudo("echo {0} >> /home/ubuntu/hadoop/etc/hadoop/masters".format(hadoop_cluster.getNode(c.hadoop_secondary_namenode).dns_name))
    sudo(">/home/ubuntu/hadoop/etc/hadoop/slaves")
    for slave in c.hadoop_slaves:
        sudo("echo {0} >> /home/ubuntu/hadoop/etc/hadoop/slaves".format(hadoop_cluster.getNode(slave).dns_name))

    for slave in c.hadoop_slaves:
        env.host_string = hadoop_cluster.getNode(slave).ip_address
        sudo("echo {0} > /home/ubuntu/hadoop/etc/hadoop/slaves".format(hadoop_cluster.getNode(slave).dns_name))

@task
def test_hadoop_master_slave_setup():
    with settings(warn_only = True):
        env.host_string = hadoop_cluster.getNode("saltmaster").ip_address
        env.user = c.aws_user
        env.key_filename = c.aws_key_location
        sudo("salt '*' cmd.run 'cat /home/ubuntu/hadoop/etc/hadoop/masters'")
        sudo("salt '*' cmd.run 'cat /home/ubuntu/hadoop/etc/hadoop/slaves'")
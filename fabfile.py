__author__ = 'rakesh.varma'
from fabric.api import *
from ConfigParser import SafeConfigParser
import ast


host_config = SafeConfigParser()
host_config.read('aws_hadoop.hosts')

main_config = SafeConfigParser()
main_config.read('config.ini')

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
    env.host_string = eval(host_config.get("main", "saltmaster"))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('add-apt-repository -y ppa:saltstack/salt')
    sudo('apt-get update')
    sudo('apt-get install -y salt-master')
    sudo('service --status-all 2>&1 | grep salt')
    sudo('salt-key -L')

@task
def salt_minion_install():

    hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
    for host in hosts:
        env.host_string = eval(host_config.get('main', host))['ip_address']
        env.user = 'ubuntu'
        env.key_filename = "~/.ssh/hadoopec2cluster.pem"
        sudo('add-apt-repository -y ppa:saltstack/salt')
        sudo('apt-get update')
        sudo('apt-get install -y salt-minion')
        cmd = 'echo "master: {0}" > /etc/salt/minion'.format(eval(host_config.get('main', 'saltmaster'))['ip_address'])
        sudo(cmd)
        sudo('echo "id: {0}" >> /etc/salt/minion'.format(host))
        sudo('service --status-all 2>&1 | grep salt')
        sudo('service salt-minion restart')

@task
def salt_master_keys_accept():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt-key -L')
    sudo('salt-key -y --accept-all')

@task
def test_salt():
    local('python -m unittest -v tests.test_salt_install')

@task
def hadoop_nodes_enable_public_access():
    hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
    for host in hosts:
        env.host_string = eval(host_config.get('main', host))['ip_address']
        env.user = 'ubuntu'
        env.key_filename = "~/.ssh/hadoopec2cluster.pem"
        cmd_change_hostname = 'hostname {0}'.format(eval(host_config.get('main', host))['dns_name'])
        sudo(cmd_change_hostname)
        cmd_change_hostfile = 'cat /etc/hosts|sed "s/localhost/{0}/"|sed "s/127.0.0.1/{1}/" >/etc/hosts'.format(eval(host_config.get('main', host))['dns_name'], format(eval(config.get('main', host))['private_ip_address']))
        sudo(cmd_change_hostfile)
        sudo('echo {0} >> /home/ubuntu/.ssh/config'.format("Host *"))
        sudo('echo {0} >> /home/ubuntu/.ssh/config'.format("    StrictHostKeyChecking no"))


@task
def test_hadoop_nodes_public_access():
    local('python -m unittest -v tests.test_hadoop_nodes_public_access')

@task
def install_jdk_hadoop_nodes():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    with settings(warn_only = True):
        sudo('salt "*" cmd.run "sudo apt-get update"')
        sudo('salt "*" cmd.run "sudo add-apt-repository ppa:webupd8team/java"')
        sudo('salt "*" cmd.run "echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections"')
        sudo('salt "*" cmd.run "sudo apt-get update && sudo apt-get install -y oracle-jdk7-installer"')
        sudo('salt "*" cmd.run "sudo apt-get -f -y -q install"')


@task
def test_java():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt "*" cmd.run "java -version"')

@task
def install_hadoop():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt "*" cmd.run "wget http://apache.mirror.gtcomm.net/hadoop/common/current/hadoop-2.7.1.tar.gz -P /home/ubuntu"')
    sudo('salt "*" cmd.run "tar -xzvf /home/ubuntu/hadoop-2.7.1.tar.gz -C /home/ubuntu"')
    sudo('salt "*" cmd.run "mv /home/ubuntu/hadoop-2.7.1 /home/ubuntu/hadoop"')
    #sudo('salt "*" cmd.run " echo {0} >> /home/ubuntu/.bashrc"'.format("export HADOOP_CONF=/home/ubuntu/hadoop/etc/hadoop"))
    #sudo('salt "*" cmd.run "source /home/ubuntu/.bashrc"')

@task
def test_hadoop():
    env.host_string = eval(host_config.get('main', 'saltmaster'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('salt "*" cmd.run "ls -lt /home/ubuntu/hadoop"')
    sudo('salt "*" cmd.run "ls -lt /usr/lib/jvm/java-7-oracle"')

@task
def setup_ssh_access():
    #ftp the hadoopec2cluster.pem to hadoopmaster at /home/ubuntu/.ssh
    #eval `ssh-agent`
    #ssh-add hadoopec2cluster.pem

    env.host_string = eval(host_config.get('main', 'hadoopnamenode'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo('eval `ssh-agent` && ssh-add /home/ubuntu/.ssh/hadoopec2cluster.pem')
    #sudo('ssh-add /home/ubuntu/hadoopec2cluster.pem')

@task
def disable_strict_host_check():
    main_config = SafeConfigParser()
    main_config.read('config.ini')
    hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
    for host in hosts:
        env.host_string = eval(host_config.get('main', host))['ip_address']
        env.user = 'ubuntu'
        env.key_filename = "~/.ssh/hadoopec2cluster.pem"
        sudo('echo {0} > /home/ubuntu/.ssh/config'.format("Host '*'"))
        sudo('echo {0} >> /home/ubuntu/.ssh/config'.format("    StrictHostKeyChecking no"))

@task
def test_ssh_access():
    env.host_string = eval(host_config.get('main', 'hadoopnamenode'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"

    main_config = SafeConfigParser()
    main_config.read('config.ini')
    hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
    for host in hosts:
        if host != 'hadoopnamenode':
            target_ip = eval(host_config.get('main', host))['ip_address']
            sudo('ssh {0}@{1}'.format("ubuntu", target_ip))

@task
def deploy_hadoop_files():
    hadoopnamenode = eval(host_config.get('main', 'hadoopnamenode'))['dns_name']

    main_config = SafeConfigParser()
    main_config.read('config.ini')
    #hosts = ast.literal_eval(main_config.get('main','hadoop_nodes'))
    hadoop_env_text = "cat /home/ubuntu/hadoop/etc/hadoop/hadoop-env.sh|sed  s/{JAVA_HOME}/\\\/usr\\\/lib\\\/jvm\\\/java-7-oracle/"
    core_site_text = """<?xml version="1.0" encoding="UTF-8"?>
                        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
                        <configuration>
                        <property>
                        <name>fs.default.name</name>
                        <value>{0}:8020</value>
                        </property>
                        <property>
                        <name>hadoop.tmp.dir</name>
                        <value>/home/ubuntu/hdfstmp</value>
                        </property>
                        </configuration>""".format(hadoopnamenode)

    hdfs_site_text ="""<?xml version="1.0" encoding="UTF-8"?>
                        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
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
    mapred_site_text ="""<configuration>
                        <property>
                        <name>mapred.job.tracker</name>
                        <value>{0}:8021</value>
                        </property>
                        </configuration>""".format(hadoopnamenode)


    env.host_string = eval(host_config.get('main', 'hadoopsecondarynamenode'))['ip_address']
    env.user = 'ubuntu'
    env.key_filename = "~/.ssh/hadoopec2cluster.pem"
    sudo(hadoop_env_text)
    #sudo('echo {0} > /home/ubuntu/hadoop/etc/hadoop/core-site.xml'.format(core_site_text))
    #sudo('echo {0} > /home/ubuntu/hadoop/etc/hadoop/hdfs-site.xml'.format(hdfs_site_text))
    #sudo('echo {0} > /home/ubuntu/hadoop/etc/hadoop/mapred-site.xml'.format(mapred_site_text))

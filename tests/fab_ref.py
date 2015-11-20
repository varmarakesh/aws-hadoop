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
            sudo('ssh {0}@{1}'.format("ubuntu", target_ip))__author__ = 'rakesh.varma'

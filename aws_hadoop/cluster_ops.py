from fabric.api import env, run, sudo
from fabric.contrib.files import exists, append, upload_template
import logging
import os


class FabricContext(object):
    """
    FabricContext object holds the properties for namenode, secondarynamenode and slaves.
    """

    def __init__(self, namenode, secondarynamenode, slaves, replication_factor=None):
        self.namenode = namenode
        self.seccondarynamenode = secondarynamenode
        self.slaves = slaves
        # default 2
        self.replication_factor = replication_factor or 2


class ClusterOps(object):

    def __init__(self, ip_address, ssh_user, ssh_use_ssh_config, ssh_proxy, ssh_keyfile, context, logger=None):
        env.use_ssh_config = ssh_use_ssh_config
        env.host_string = ip_address
        env.user = ssh_user
        env.key_filename = ssh_keyfile
        env.gateway = ssh_proxy

        self.context = context
        self.logger = logger or logging.getLogger(__name__)

    @property
    def _context(self):
        return {
            'hadoop': {
                'namenode': self.context.namenode,
                'slaves': self.context.slaves,
                'dfs_replication': self.context.replication_factor,
                'java_home': '/usr/lib/jvm/java-8-oracle'
            }
        }

    def create_public_key(self):
        """
        Create ssh key pair (id_rsa, id_rsa.pub and returns id_rsa.pub)
        :return:
        """
        rsa_private_key_path = '/home/ubuntu/.ssh/id_rsa'
        rsa_public_key_path = '/home/ubuntu/.ssh/id_rsa.pub'
        ssh_config_path = '/home/ubuntu/.ssh/config'

        # Skip if already exists, else create keys
        if (exists(rsa_private_key_path, use_sudo=False) and exists(rsa_public_key_path, use_sudo=False)) == False:
            run('ssh-keygen -t rsa -f {0} -q -N ""'.format(rsa_private_key_path))
            self.logger.info(msg="RSA key pair created.")
        else:
            self.logger.info(msg="RSA key pair already exists.")

        # adding StrictHostKeyChecking no in the .ssh/config file so that ssh login is not prompted.
        run('echo "{0}" > {1}'.format("Host *", ssh_config_path))
        run('echo "{0}" >> {1}'.format("   StrictHostKeyChecking no", ssh_config_path))
        public_key = sudo('cat {0}'.format(rsa_public_key_path))
        return public_key

    def set_authorized_key(self, public_key):
        """
        Adds public_key to authorized_keys file.
        :param public_key:
        :return:
        """
        authorized_keys_path = '/home/ubuntu/.ssh/authorized_keys'
        append(authorized_keys_path,text=public_key,use_sudo=True,partial=False,escape=False)
        self.logger.info(msg="Public key added to authorized_keys")

    def apply_hadoop_env_template(self):
        upload_template(
            'hadoop-env.sh',
            destination='/home/ubuntu/hadoop/etc/hadoop/hadoop-env.sh',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup = False,
            context = self._context
        )
        self.logger.info(msg="hadoop-env.sh updated")

    def apply_core_site_template(self):
        upload_template(
            'core-site.xml',
            destination='/home/ubuntu/hadoop/etc/hadoop/core-site.xml',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup = False,
            context = self._context
        )
        self.logger.info(msg="core-site.xml updated")

    def apply_hdfs_site_template(self):
        upload_template(
            'hdfs-site.xml',
            destination='/home/ubuntu/hadoop/etc/hadoop/hdfs-site.xml',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup=False,
            context=self._context
        )
        self.logger.info(msg="hdfs-site.xml updated")

    def apply_mapred_site_template(self):
        upload_template(
            'mapred-site.xml',
            destination='/home/ubuntu/hadoop/etc/hadoop/mapred-site.xml',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup=False,
            context=self._context
        )
        self.logger.info(msg="mapred-site.xml updated")

    def apply_slave_template(self):
        upload_template(
            'slaves',
            destination='/home/ubuntu/hadoop/etc/hadoop/slaves',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup=False,
            context=self._context
        )
        self.logger.info(msg="slaves config updated")

    def apply_masters_template(self):
        upload_template(
            'masters',
            destination='/home/ubuntu/hadoop/etc/hadoop/masters',
            use_jinja=True,
            template_dir=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            backup=False,
            context=self._context
        )
        self.logger.info(msg="masters config updated")

    def hadoop_master_start_services(self):
        run("/home/ubuntu/hadoop/bin/hadoop namenode -format -force")
        run("/home/ubuntu/hadoop/sbin/start-dfs.sh")
        run("jps")


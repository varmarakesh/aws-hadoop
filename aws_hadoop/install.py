from aws_hadoop.terraform import TerraformHadoop
from aws_hadoop.logger import Logger
from aws_hadoop.cluster_ops import ClusterOps, FabricContext
from aws_hadoop.config import ConfigFactory


class Install(object):
    """
    Install class offers create, destroy API's.
    """

    def __init__(self, configFile=None):
        self.logger = Logger(
            log_file='hadoop-cluster.log'
        ).getLogger()

        self.config = ConfigFactory(configFile=configFile, logger=self.logger)
        self.tf = TerraformHadoop(
            aws_profile=self.config.aws_profile,
            s3_bucket=self.config.terraform_s3_bucket,
            tf_vars=self.config.get_tf_vars(),
            logger=self.logger
        )

    def create(self):
        """
        Create methods runs TF apply to create AWS resources and
        provisions the cluster using fabric.
        :return:
        """

        self.logger.info(
            msg='Starting the hadoop cluster provisioning process.'
        )
        self.tf.apply()
        ctx = FabricContext(
            namenode=self.tf.hadoop_namenode_ip,
            secondarynamenode=self.tf.hadoop_secondarynamenode_ip,
            slaves=self.tf.hadoop_datanodes_ips,
            replication_factor=self.config.hadoop_replication_factor
        )

        self.logger.info(
            msg='Connecting to Hadoop Namenode - {0} for applying the templates.'.format(
                self.tf.hadoop_namenode_ip
            )
        )
        namenode = ClusterOps(
            ip_address=self.tf.hadoop_namenode_ip,
            ssh_user=self.config.ssh_user,
            ssh_keyfile=self.config.ssh_keyfile,
            ssh_use_ssh_config=self.config.ssh_use_ssh_config,
            ssh_proxy=self.config.ssh_proxy,
            context=ctx,
            logger=self.logger
        )
        public_key = namenode.create_public_key()
        namenode.set_authorized_key(public_key=public_key)
        namenode.apply_hadoop_env_template()
        namenode.apply_core_site_template()
        namenode.apply_hdfs_site_template()
        namenode.apply_mapred_site_template()
        namenode.apply_masters_template()
        namenode.apply_slave_template()

        self.logger.info(msg='Connecting to Hadoop SecondaryNamenode - {0} for applying the templates'.format(self.tf.hadoop_secondarynamenode_ip))
        secondarynamenode = ClusterOps(
            ip_address=self.tf.hadoop_secondarynamenode_ip,
            ssh_user=self.config.ssh_user,
            ssh_keyfile=self.config.ssh_keyfile,
            ssh_use_ssh_config=self.config.ssh_use_ssh_config,
            ssh_proxy=self.config.ssh_proxy,
            context=ctx,
            logger=self.logger
        )
        secondarynamenode.set_authorized_key(public_key=public_key)
        secondarynamenode.apply_hadoop_env_template()
        secondarynamenode.apply_core_site_template()
        secondarynamenode.apply_hdfs_site_template()
        secondarynamenode.apply_mapred_site_template()
        secondarynamenode.apply_masters_template()
        secondarynamenode.apply_slave_template()

        for datanode in self.tf.hadoop_datanodes_ips:
            self.logger.info(msg='Connecting to Hadoop Datanode - {0} for applying the templates'.format(datanode))
            slave = ClusterOps(
                ip_address=datanode,
                ssh_user=self.config.ssh_user,
                ssh_keyfile=self.config.ssh_keyfile,
                ssh_use_ssh_config=self.config.ssh_use_ssh_config,
                ssh_proxy=self.config.ssh_proxy,
                context=ctx,
                logger=self.logger
            )
            slave.set_authorized_key(public_key=public_key)
            slave.apply_hadoop_env_template()
            slave.apply_core_site_template()
            slave.apply_hdfs_site_template()
            slave.apply_mapred_site_template()
            slave.apply_slave_template()

        self.logger.info(msg='Connecting to Hadoop Namenode - {0} for formatting DFS and starting cluster'.format(self.tf.hadoop_namenode_ip))
        namenode = ClusterOps(
            ip_address=self.tf.hadoop_namenode_ip,
            ssh_user=self.config.ssh_user,
            ssh_keyfile=self.config.ssh_keyfile,
            ssh_use_ssh_config=self.config.ssh_use_ssh_config,
            ssh_proxy=self.config.ssh_proxy,
            context=ctx,
            logger=self.logger
        )
        namenode.hadoop_master_start_services()
        self.logger.info(msg='Exiting aws_hadoop.')

    def destroy(self):
        """
        Destroy methods runs TF destroy to remove all AWS resources.
        :return:
        """
        self.logger.info(msg='Destroying the AWS resources.')
        self.tf.destroy()

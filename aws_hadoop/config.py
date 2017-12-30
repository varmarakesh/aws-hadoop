from ConfigParser import SafeConfigParser, NoOptionError
import logging
from sets import Set
from ast import literal_eval


class ConfigFactory(object):
    """
    This class implements properties for all the configuration parameters.
    """

    def __init__(self, configFile=None, logger=None):
        self.config = SafeConfigParser()
        self.logger = logger or logging.getLogger(__name__)
        self._set_config(configFile=configFile)
        self.section = 'default'
        self._validate()

    def _set_config(self, configFile):
        """
        sets the config file.
        :param configFile:
        :return:
        """
        if configFile:
            self.logger.info(msg='Parsing config file - {0}'.format(configFile))
        else:
            self.logger.info(msg='config file not specified, so using the config.ini in the current working directory.')
            configFile = 'config.ini'

        self.config.read(configFile)
        if not self.config.has_section("default"):
            self.logger.error(msg='config file {0} missing default section or cannot be found. Exiting.'.format(configFile))
            exit(1)

    def _validate(self):
        """
        validates the presence of all mandatory fields in the config file.
        :return:
        """
        mandatory_config_fields = Set(
            [
                'aws_profile',
                'aws_region',
                'terraform_s3_bucket',
                'ssh_private_key',
                'vpc_id',
                'vpc_subnets'
            ]
        )
        all_config_fields = Set([k for k,v in self.config.items('default')])
        if not mandatory_config_fields.issubset(all_config_fields):
            self.logger.error(msg='Mandatory fields missing from config file - {0}, exiting...'.format(
                mandatory_config_fields - all_config_fields
            ))
            exit(1)
        else:
            self.logger.info(msg='config file successfully validated for mandatory items.')

    @property
    def aws_profile(self):
        return self.config.get(
            section=self.section,
            option='aws_profile'
        )

    @property
    def aws_region(self):
        return self.config.get(
            section=self.section,
            option='aws_region'
        )

    @property
    def terraform_s3_bucket(self):
        return self.config.get(
            section=self.section,
            option='terraform_s3_bucket'
        )

    @property
    def ssh_private_key(self):
        return self.config.get(
            section=self.section,
            option='ssh_private_key'
        )

    @property
    def vpc_id(self):
        return self.config.get(
            section=self.section,
            option='vpc_id'
        )

    @property
    def hadoop_namenode_instance_type(self):
        try:
            return self.config.get(
                section=self.section,
                option='hadoop_namenode_instance_type'
            )
        except NoOptionError:
            self.logger.warn(
                msg='No hadoop_namenode_instance_type option found in config, so using a default of t2.micro'
            )
            return 't2.micro'

    @property
    def hadoop_secondarynamenode_instance_type(self):
        try:
            return self.config.get(
                section=self.section,
                option='hadoop_secondarynamenode_instance_type'
            )
        except NoOptionError:
            self.logger.warn(
                msg='No hadoop_secondarynamenode_instance_type option found in config, so using a default of t2.micro'
            )
            return 't2.micro'

    @property
    def hadoop_datanodes_instance_type(self):
        try:
            return self.config.get(
                section=self.section,
                option='hadoop_datanodes_instance_type'
            )
        except NoOptionError:
            self.logger.warn(
                msg='No hadoop_datanodes_instance_type option found in config, so using a default of t2.micro'
            )
            return 't2.micro'

    @property
    def hadoop_datanodes_count(self):
        try:
            return self.config.get(
                section=self.section,
                option='hadoop_datanodes_count'
            )
        except NoOptionError:
            self.logger.warn(
                msg='No hadoop_datanodes_count option found in config, so using a default of 2'
            )
            return 2

    @property
    def private_subnets(self):
        return literal_eval(
            self.config.get(
                section=self.section,
                option='vpc_subnets'
        )   )

    @property
    def hadoop_replication_factor(self):
        try:
            return self.config.get(
                section=self.section,
                option='hadoop_replication_factor'
            )
        except NoOptionError:
            self.logger.warn(
                msg='No hadoop_replication_factor option found in config, so using a default of 2'
            )
            return 2

    @property
    def ssh_use_ssh_config(self):
        try:
            return self.config.get(
                section=self.section,
                option='ssh_use_ssh_config'
            )
        except NoOptionError:
            return None

    @property
    def ssh_user(self):
        try:
            return self.config.get(
                section=self.section,
                option='ssh_user'
            )
        except NoOptionError:
            return None

    @property
    def ssh_keyfile(self):
        try:
            return self.config.get(
                section=self.section,
                option='ssh_keyfile'
            )
        except NoOptionError:
            return None

    @property
    def ssh_proxy(self):
        try:
            return self.config.get(
                section=self.section,
                option='ssh_proxy'
            )
        except NoOptionError:
            return None

    def get_tf_vars(self):
        tf_vars = {
            'ssh_private_key': self.ssh_private_key,
            'vpc_id': self.vpc_id,
            'hadoop_namenode_instance_type': self.hadoop_namenode_instance_type,
            'hadoop_secondarynamenode_instance_type': self.hadoop_secondarynamenode_instance_type,
            'hadoop_datanodes_instance_type': self.hadoop_datanodes_instance_type,
            'slave_count': self.hadoop_datanodes_count,
            'private_subnets': self.private_subnets
        }
        return tf_vars

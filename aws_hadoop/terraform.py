from python_terraform import *
import os
import logging


class TerraformHadoop(object):
    """
    TerraformHadoop uses python_terraform and provides a pythonic interface
    to all the terraform operations.
    """

    def __init__(self, aws_profile, s3_bucket, tf_vars, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.tf_vars = tf_vars
        self.s3_bucket = s3_bucket
        os.environ['AWS_PROFILE'] = aws_profile
        # Because of abspath, this module could be run from anywhere.
        terraform_working_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'terraform'
        )
        self.tf = Terraform(working_dir=terraform_working_dir)

    def _initialize(self):
        os.environ['AWS_PROFILE'] = self.aws_profile

    def _log_tf_result(self, return_code, stdout, stderr, operation):
        """
        log TF apply/destroy output
        :param return_code:
        :param stdout:
        :param stderr:
        :param operation:
        :return:
        """
        if return_code:
            self.logger.info(
                'Terraform {0} return code - {1}'.format(
                    operation,
                    return_code
                )
            )
            self.logger.info(stderr)
        else:
            self.logger.info('Terraform {0} successful'.format(operation))
            self.logger.info(stdout)

    def plan(self):
        """
        Runs TF plan
        :return:
        """
        self.tf.init(backend_config='bucket={0}'.format(self.s3_bucket))
        self.logger.info('Terraform Initialized. Running Terraform plan...')
        return_code, stdout, stderr = self.tf.plan(var=self.tf_vars)
        self._log_tf_result(return_code, stdout, stderr, 'plan')
        return return_code, stdout, stderr

    def apply(self):
        """
        Run TF apply
        :return:
        """
        self.tf.init(backend_config='bucket={0}'.format(self.s3_bucket))
        self.logger.info('Terraform Initialized. Running Terraform apply...')
        return_code, stdout, stderr = self.tf.apply(var=self.tf_vars)
        self._log_tf_result(return_code, stdout, stderr, 'apply')

    def destroy(self):
        """
        Destroy the TF states without any warning.
        :return:
        """
        self.tf.init(backend_config='bucket={0}'.format(self.s3_bucket))
        self.logger.info('Terraform Initialized. Running Terraform destroy...')
        return_code, stdout, stderr = self.tf.destroy(var=self.tf_vars)
        self._log_tf_result(return_code, stdout, stderr, 'destroy')

    @property
    def hadoop_namenode_ip(self):
        return self.tf.output('hadoop-namenode_ip').strip()

    @property
    def hadoop_secondarynamenode_ip(self):
        return self.tf.output('hadoop-secondarynamenode_ip').strip()

    @property
    def hadoop_datanodes_ips(self):
        return self.tf.output('hadoop-datanode_ips')

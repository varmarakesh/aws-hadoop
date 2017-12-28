import unittest
from aws_hadoop.config import ConfigFactory
from aws_hadoop.terraform import TerraformHadoop

class Terraform(unittest.TestCase):

    def setUp(self):
        self.config = ConfigFactory()
        self.tf = TerraformHadoop(
            aws_profile=self.config.aws_profile,
            s3_bucket=self.config.terraform_s3_bucket,
            tf_vars=self.config.get_tf_vars()
        )

    def test_tf_plan(self):
        """
        Testing plan and asserting return_code is 0
        :return:
        """
        return_code, stdout, stderr = self.tf.plan()
        import pdb
        pdb.set_trace()
        self.assertEquals(return_code,0)


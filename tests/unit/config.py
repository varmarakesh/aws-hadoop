import unittest
from ConfigParser import SafeConfigParser, NoOptionError
from ast import literal_eval
from types import ListType, StringType

class Config(unittest.TestCase):

    def test_config_does_not_exist(self):
        """
        test.ini does not exist, config.has_section can be used to check the presence of config file.
        :return:
        """
        config = SafeConfigParser()
        config.read('test.ini')
        self.assertFalse(config.has_section('default'))

    def test_config_list(self):
        """
        Check to ensure list item can be loaded from the config file using literal_eval
        :return:
        """
        config = SafeConfigParser()
        config.read('config.ini')
        self.assertTrue(
            type(literal_eval(config.get(section='default',option='vpc_subnets'))) is ListType
        )

    def test_config_list_item_type(self):
        """
        As an extension to previous test, check that the first item of the vpc_subnets list is of type string.
        """
        config = SafeConfigParser()
        config.read('config.ini')
        self.assertTrue(
            type(literal_eval(config.get(section='default',option='vpc_subnets'))[0]) is StringType
        )

    def test_config_items_not_exist_exception(self):
        """
        Validate NoOptionError is thrown when config item does not exist.
        """
        config = SafeConfigParser()
        config.read('config.ini')
        self.assertRaises(NoOptionError,config.get,'default','doesnotexistoption')

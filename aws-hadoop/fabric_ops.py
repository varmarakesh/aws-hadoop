__author__ = 'rakesh.varma'
from fabric.api import *
import os
import time

class fabric_ops:

    def __init__(self, host_ip, host_user, host_key_file):
        env.host_string = host_ip
        env.user = host_user
        env.key_filename = host_key_file
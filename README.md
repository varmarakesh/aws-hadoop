Create Enterprise grade Hadoop cluster in AWS.
===============================

author: Rakesh Varma

Overview
--------

Create enterprise grade hadoop cluster in AWS in minutes.

Using this solution as one-stop shop to create AWS resources needed for hadoop (ec2, security groups) and setup a cluster with Hadoop namenode, secondarynamenode and any number of data nodes.

The ec2 nodes use:

* ubuntu - 16.04.3 LTS
* hadoop - 2.9.0
* java - 8

Installation / Usage
--------------------

Make sure [terraform](https://www.terraform.io/intro/getting-started/install.html) is installed. It is required to run this solution.

Make sure AWS credentials exists in your local `~/.aws/credentials` file. 
If you are using an `AWS_PROFILE` called `test` then your `credentials` file should like looks this:

```sh
[test]
aws_access_key_id = SOMEAWSACCESSKEYID
aws_secret_access_key = SOMEAWSSECRETACCESSKEY
```

Create a `config.ini` with the appropriate settings.

```sh
[default]

# AWS settings
aws_region = us-east-1
aws_profile = test
terraform_s3_bucket = hadoop-terraform-state
ssh_private_key = key.pem
vpc_id = vpc-883883883
vpc_subnets = [
                'subnet-89dad652',
                'subnet-7887z892',
                'subnet-f300b8z8'
              ]
hadoop_namenode_instance_type = t2.micro
hadoop_secondarynamenode_instance_type = t2.micro
hadoop_datanodes_instance_type = t2.micro
hadoop_datanodes_count = 2

# Hadoop settings
hadoop_replication_factor = 2
```

Once `config.ini` file is ready then install the libs and run. It is recommended to use a virtualenv.

```
   pip install aws-hadoop
```
Run this in python to create a hadoop cluster.
```
from aws_hadoop.install import Install
Install().create()
```

For running the source directly,

```sh
pip install -r requirements.txt
```
```sh
from aws_hadoop.install import Install
Install().create()
```

### Configuration Settings

This section describes each of the settings that go into the config file. Note some of the settings are optional.

###### aws_region

The aws_region where your terraform state bucket and your hadoop resources get created (eg: us-east-1)

##### aws_profile

The aws_profile that is used in your local `~/.aws/credentials` file.

##### terraform_s3_bucket

The terraform state information will be maintained in the specified s3 bucket. Make sure the aws_profile has write access to the s3 bucket.

##### ssh_key_pair

For hadoop provisioning, aws_hadoop needs to connect to hadoop nodes using SSH. The specified `ssh_key_pair` will allow the hadoop ec2's to be created with the public key.
If So make sure your machine has the private key in your `~/.ssh/` directory.

##### vpc_id

Specifiy the vpc id your AWS region in which the terraform resources should be created.

##### vpc_subnets

vpc_subnets is a list item that contains one or more subnet_id's. You can specify as many subnet id's as you want. Hadoop EC2 will get created in multiple subnets.

##### hadoop_namenode_instance_type (optional)

Specify the instance type of hadoop namenode. It not specified then the default instance type is `t2.micro`

##### hadoop_secondarynamenode_instance_type (optional)

Specify the instance type of hadoop secondarynamenode. It not specified then the default instance type is t2.micro

##### hadoop_datanodes_instance_type (optional)

Specify the instance type of hadoop datanodes. It not specified then the default instance type is t2.micro

##### hadoop_datanodes_count (optional)

Specify the number of hadoop data nodes that should be created. It not specified then the default value is set to 2

##### hadoop_replication_factor (optional)

Specify the replication factor of hadoop. It not specified then the default value is set to 2.

The following are ssh settings, used to ssh into the nodes.

##### ssh_user (optional)
The ssh user, eg: ubuntu

##### ssh_use_ssh_config (optional)
Set it to True if you want to use your settings in your `~/.ssh/config`

##### ssh_key_file (optional)
This is the key file location. SSH login is done thru a private/public key pair.

##### ssh_proxy (optional)
Use this setting if you are using a proxy ssh server (such as bastion).

Logging
------

A log file `hadoop-cluster.log` is created in the local directory.

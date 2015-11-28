#aws-hadoop

The purpose of this project is to fully automate the creation of a hadoop cluster in amazon ec2. This includes creation of ubuntu instances, installing 
hadoop packages and it is pre-requisites, setting up access between nodes and deploying hadoop configs to nodes. It also includes setting up saltstack for configuration management of hadoop nodes.

##Project goals


1. Provision hadoop cluster in AWS EC2 with any number of nodes in less than 5 minutes.
2. Architect the solution so that it is easy to install and run. Create tests so that failures at each step can be easily diagnosed.
3. Provide the user to configure various options such as number of slaves in hadoop cluster, aws instance type, aws region.

##Install Instructions

1. Clone the project to your machine. Make sure git is installed first.
    *   git --version
    *   git clone https://github.com/varmarakesh/aws-hadoop.git
2. Verify python 2.7 in installed. Also verify pip is installed.
    *   python --version
    *   pip --version
    pip is the package manager for installing python packages. Next step uses pip to install the python packages needed to run this project.
3. Install the python packages, boto and fabric that are required to run this project. Running pip on requirements.txt will install the packages.
    *    cd aws-hadoop
    *    pip install -r requirements.txt
4. Edit settings in config.ini. To make it work you can leave everything as they are except these settings. The right values have to be specified for these settings.
    
    Create aws access key. for more information on creating aws keys refer to this link.
    http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
    
    *   aws_access_key_id
    *   aws_secret_access_key
    
    create a key pair in aws. for more information refer to this link.
    http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair
    
    Once you create a key pair you can download the .pem to your local file system. specify the full path for this item.
    
    *   aws_key_location
    
    Also, specify the AWS security group. For more information on security group, refer to this link
    for more information on creating aws keys refer to this link.
    http://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html
    
    *   aws_security_group
    
    As needed make changes to hadoop_nodes to add namenode, secondarynamenode and slaves.
    
5. At this point, the setup is complete and you can begin your hadoop cluster provisioning by simply running.
    *   fab provision_hadoop_cluster

##Platform Tests

   So far, this has been successfully tested on the following platforms.
   
   *    mac osx 10.9
   *    ubuntu server 14.04
# aws-hadoop

The purpose of this project is to fully automate the creation of a hadoop cluster in amazon ec2. This includes creation of ubuntu instances, installing 
hadoop packages and it is pre-requisites, setting up access between nodes and deploying hadoop configs to nodes. It also includes setting up saltstack for configuration management of hadoop nodes.

Project goals

1. Provision hadoop cluster in AWS EC2 with any number of nodes in less than 2 minutes.
2. Architect the solution so that it is easy to install and run. Create tests so that failures at each step can be easily diagnosed.
3. Provide the user to configure various options such as number of slaves in hadoop cluster, aws instance type, aws region.

Install Instructions.

1. Clone the project to your machine.
    git clone https://github.com/varmarakesh/aws-hadoop.git
2. Verify python 2.7 in installed. Also verify pip is installed.
    python --version
    pip --version
    pip is the package manager for installing python packages. Next step uses pip to install the 2 python packages needed to run this project.
3. Install the python packages, boto and fabric that are required to run this project. Running pip on requirements.txt will install the packages.
   cd aws-hadoop
   pip install -r requirements.txt
4. Edit settings in config.ini. You can leave everything as they are except these settings.
    aws_access_key_id
    aws_secret_access_key
    aws_key_location
  
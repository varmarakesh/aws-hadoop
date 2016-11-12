aws-hadoop
=======================
Python project that automates the setup of hadoop cluster

Usage
-----
Use this solution to create a hadoop cluster with any number of data nodes.
Installation
------------
Please do the following to run this solution.

 1. Create a number of ubuntu machines (1 for saltmaster, 1 for hadoop name node, 1 for hadoop secondaryname node, and the remaining for hadoop data nodes) in AWS. Make sure you allow all the tcp ports (these are used for communication - 22, 50070, 50090, 8021, 8020)

	To automate this step, follow these steps to use the cloud formation template.

	Create a AWS keypair pem file that will allow you to ssh to AWS EC2 instances
	open aws-hadoop/aws-cloudformation-template/hadoop.json, 
	Replace testkey with your AWS keypair. "KeyName": "testkey",
	The template has 5 ubuntu nodes (1 for saltmaster, 1 for hadoopnamenode, 1 for secondarynamenode and 2 datanodes). Add more datanodes as required.

	Once your template is ready, login to AWS management console, go to cloud formation, create stack and upload the template to create the hadoop cluster. Verify that all the ubuntu nodes are created.




2. clone the git project
    ```
git clone https://github.com/varmarakesh/aws-hadoop
    ```
    
5. Install the python libraries (suggest using virtualenv for setting up python libraries)
    ```
        cd aws-hadoop
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
    ```
    
6.  Edit the config.ini file to specify the ip's or public dns names of saltmaster, hadoop namenode, hadoop secondary namenode and hadoop datanodes. Assuming there is a key based login, also specify the key location.
7. Now in aws-hadoop/aws-hadoop, run

    ```
        fab hadoop.provision_hadoop_cluster
    ```

Compatibility
-------------

Licence
-------

Authors
-------

`aws-hadoop` was written by `Rakesh Varma <varma.rakesh@gmail.com>`_.

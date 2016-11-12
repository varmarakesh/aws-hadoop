automate-hadoop-cluster
=======================


Python project that automates the setup of hadoop cluster

Usage
-----
Use this solution to create a hadoop cluster with any number of data nodes.
Installation
------------
Please do the following to run this solution.

1. Create a number of ubuntu machines (1 for saltmaster, 1 for hadoop name node, 1 for hadoop secondaryname node, and the remaining for hadoop data nodes)
2. Create a ubuntu account on all the nodes that has sudo access
3. Make sure you allow all the tcp ports (these are used for communication - 22, 50070, 50090, 8021, 8020)
4. clone the git project
    ```
        git clone https://github.com/varmarakesh/automate-hadoop-cluster
    ```
5. Install the python libraries (suggest use virtualenv for setting up python libraries)
    ```
        cd automate-hadoop-cluster
        virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
    ```
6.  Edit the config.ini file to specify the ip's or public dns names of saltmaster, hadoop namenode, hadoop secondary namenode and hadoop datanodes. Assuming there is a key based login, also specify the key location.
7. Now in automate-hadoop-cluster/automate-hadoop-cluster, run
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

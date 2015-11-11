__author__ = 'rakesh.varma'
import boto.ec2
#boto.set_stream_logger('boto')
ec2 = boto.ec2.connect_to_region('us-west-2', aws_access_key_id = 'AKIAIAWIUPFHWRWHEN4Q', aws_secret_access_key = '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')

reservation = ec2.run_instances('ami-5189a661',
                     key_name='hadoopcluster',
                     instance_type='t2.micro',
                     security_groups=['HadoopEC2SecurityGroup'],
                     min_count = 4, max_count=4)

reservation.instances[0].add_tag("Name", "HadoopNameNode")
reservation.instances[1].add_tag("Name", "HadoopSecondaryNameNode")
reservation.instances[2].add_tag("Name", "HadoopSlave1")
reservation.instances[3].add_tag("Name", "HadoopSlave2")


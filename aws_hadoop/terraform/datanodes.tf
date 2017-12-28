resource "aws_instance" "hadoop-datanode" {
  count                  = 2
  ami                    = "${data.aws_ami.hadoop.id}"
  instance_type          = "${var.hadoop_datanodes_instance_type}"
  subnet_id              = "${element(var.private_subnets, count.index)}"
  key_name               = "${var.ssh_private_key}"
  vpc_security_group_ids = [
    "${aws_security_group.hadoop.id}"
  ]
  root_block_device {
    volume_type = "gp2"
    volume_size = "20"
  }
  tags {
    Name                 =   "hadoop-datanode-${count.index}"
  }
}

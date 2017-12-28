
# SG for hadoop
resource "aws_security_group" "hadoop" {
  name        = "hadoop"
  description = "SG for hadoop"
  vpc_id      = "${var.vpc_id}"

  tags {
    Name      = "hadoop"
  }
}

resource "aws_security_group_rule" "hadoop-all-ingress" {
  type              = "ingress"
  from_port         = "0"
  to_port           = "0"
  protocol          = "all"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.hadoop.id}"
}


# Allow outbound traffic to anywhere
resource "aws_security_group_rule" "hadoop-all-outgress" {
  type                     = "egress"
  from_port                = 0
  to_port                  = 0
  protocol                 = "all"
  cidr_blocks              = ["0.0.0.0/0"]
  security_group_id        = "${aws_security_group.hadoop.id}"
}

# Hadoop Namenode EC2
resource "aws_instance" "hadoop-namenode" {
  ami                    = "${data.aws_ami.hadoop.id}"
  key_name               = "${var.ssh_private_key}"
  subnet_id              = "${element(var.private_subnets, 1)}"
  instance_type          = "${var.hadoop_namenode_instance_type}"
  vpc_security_group_ids = [
    "${aws_security_group.hadoop.id}"
  ]

  root_block_device {
    volume_type = "gp2"
    volume_size = "20"
  }

  tags {
    Name        = "hadoop-namenode"
  }
}

# Hadoop Secondary Namenode EC2
resource "aws_instance" "hadoop-secondarynamenode" {
  ami                    = "${data.aws_ami.hadoop.id}"
  key_name               = "${var.ssh_private_key}"
  subnet_id              = "${element(var.private_subnets, 1)}"
  instance_type          = "${var.hadoop_secondarynamenode_instance_type}"
  vpc_security_group_ids = [
    "${aws_security_group.hadoop.id}"
  ]

  root_block_device {
    volume_type = "gp2"
    volume_size = "20"
  }

  tags {
    Name        = "hadoop-secondarynamenode"
  }
}


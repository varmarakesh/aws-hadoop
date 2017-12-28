# Common AMI data resources

# Latest Ubuntu 16.04
data "aws_ami" "hadoop" {
  most_recent = true
  owners      = ["086212508043"]

  filter {
    name   = "name"
    values = ["hadoop-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

variable "ssh_private_key" {
  type = "string"
}

variable "hadoop_namenode_instance_type"{
  type = "string"
}

variable "hadoop_secondarynamenode_instance_type"{
  type = "string"
}

variable "hadoop_datanodes_instance_type"{
  type = "string"
}

variable "vpc_id" {
  type = "string"
}

variable "slave_count"{
}

variable "private_subnets"{
  type = "list"
}

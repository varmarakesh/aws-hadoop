output "hadoop-namenode_ip" {
  value = "${aws_instance.hadoop-namenode.private_ip}"
}

output "hadoop-secondarynamenode_ip" {
  value = "${aws_instance.hadoop-secondarynamenode.private_ip}"
}

output "hadoop-datanode_ips" {
  value       = ["${aws_instance.hadoop-datanode.*.private_ip}"]
}

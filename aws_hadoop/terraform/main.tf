# Terraform config for Hadoop

terraform {

  backend "s3" {
    key        = "hadoop/terraform.tfstate"
    region     = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

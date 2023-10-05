variable "aws_region" {
  default = "eu-west-1"
}

variable "tags" {
  default = {
    "environment" = "kinesis"
  }
}

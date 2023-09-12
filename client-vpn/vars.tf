variable "cert_dir" {
  default = "certs"
}

variable "aws_region" {
  default = "us-west-1"
}

variable "number_azs" {
  default = 1
}

variable "dns_servers" {
  default = ["8.8.8.8"]
}

variable "vpn_client_CIDR" {
  default = "10.20.0.0/22"
}

variable "vpc_CIDR" {
  default = "172.20.0.0/16"
}

variable "split_tunnel" {
  default = false
}

variable "transport_protocol" {
  default = "UDP"
}

variable "tags" {
  default = {
    "environment" = "ovpn"
  }
}

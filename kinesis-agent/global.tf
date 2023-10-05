terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws",
      version = "5.19.0"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  region            = var.aws_region
  global_tags       = var.tags
  #  Always use 1 AZ to decrease billing costs
  availability_zone = data.aws_availability_zones.available.names[0]
}

provider "aws" {
  region = local.region
}

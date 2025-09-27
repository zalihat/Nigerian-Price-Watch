terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.9.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

module "ecr" {
  source          = "../../modules/ecr"
  repository_name = "clean-food-price-data"
}

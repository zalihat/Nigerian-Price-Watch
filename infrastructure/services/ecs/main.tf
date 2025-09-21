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

# services/ecs/main.tf
data "terraform_remote_state" "ecr" {
  backend = "local"
  config = {
    path = "../ecr/terraform.tfstate"
  }
}
module "ecs_fargate" {
  source          = "../../modules/ecs-fargate"
  region          = "eu-west-1"
  cluster_name    = "price-watch-cluster"
  service_name    = "data-cleaner"
  container_name  = "data-cleaner"
  container_port  = 8080
  cpu             = 256
  memory          = 512
#   desired_count   = 1
  image_url = "${data.terraform_remote_state.ecr.outputs.repository_url}:latest"
  
}

provider "aws" {
  region = "us-east-1"
}

module "ecs_fargate" {
  source          = "../../modules/ecs-fargate"
  region          = "us-east-1"
  cluster_name    = "price-watch-cluster"
  service_name    = "data-cleaner"
  container_name  = "data-cleaner"
  container_port  = 8080
  cpu             = 256
  memory          = 512
  desired_count   = 1
  image_url = "${module.ecr.repository_url}:latest"
  
}

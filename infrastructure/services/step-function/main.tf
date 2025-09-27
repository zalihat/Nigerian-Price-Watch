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

data "terraform_remote_state" "lambda" {
  backend = "local"
  config = {
    path = "../lambda_ingest/terraform.tfstate"
  }
}

data "terraform_remote_state" "ecs" {
  backend = "local"
  config = {
    path = "../ecs/terraform.tfstate"
  }
}

data "terraform_remote_state" "crawler" {
  backend = "local"
  config = {
    path = "../glue-crawler/terraform.tfstate"
  }
}


module "price_watch_step" {
  source                  = "../../modules/step-function"
  state_machine_name      = "price-watch-sm"
  lambda_function_arn = data.terraform_remote_state.lambda.outputs.lambda_function_arn
 
  ecs_cluster_arn = data.terraform_remote_state.ecs.outputs.cluster_arn
  
  ecs_task_definition_arn = data.terraform_remote_state.ecs.outputs.task_definition_arn
  
  ecs_subnet_ids = data.terraform_remote_state.ecs.outputs.subnet_ids
  
  ecs_security_group_ids = [data.terraform_remote_state.ecs.outputs.security_group_id]

  glue_crawler_name = data.terraform_remote_state.crawler.outputs.crawler_name
}

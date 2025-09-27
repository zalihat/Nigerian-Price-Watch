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

data "terraform_remote_state" "step_function" {
  backend = "local"
  config = {
    path = "../step-function/terraform.tfstate"
  }
}

data "terraform_remote_state" "crawler" {
  backend = "local"
  config = {
    path = "../glue-crawler/terraform.tfstate"
  }
}

module "monitoring" {
  source              = "../../modules/monitoring"
  project_name        = "price-watch"
  alert_email          = "zalihatmohammed@gmail.com"
  lambda_function_name = data.terraform_remote_state.lambda.outputs.lambda_function_name
  ecs_cluster_name     = data.terraform_remote_state.ecs.outputs.cluster_name
  step_function_arn    = data.terraform_remote_state.step_function.outputs.step_function_arn
  glue_crawler_name    = data.terraform_remote_state.crawler.outputs.crawler_name
  ecs_log_group_name = data.terraform_remote_state.ecs.outputs.ecs_log_group_name

}

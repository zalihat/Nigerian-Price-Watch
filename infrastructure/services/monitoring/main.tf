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


module "monitoring" {
  source              = "../../modules/monitoring"
  project_name        = "price-watch"
  lambda_function_name = "ingest_data_lambda"
  ecs_cluster_name     = "price-watch-cluster"
  step_function_arn    = "arn:aws:states:eu-west-1:123456789012:stateMachine:price-watch-sm"
  glue_crawler_name    = "crawl_silver_bucket"
  alert_email          = "zalihatmohammed@gmail.com"
  ecs_log_group_name = "/ecs/data-cleaner"
}

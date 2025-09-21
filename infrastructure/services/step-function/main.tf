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

module "price_watch_step" {
  source                  = "../../modules/step-function"
  state_machine_name      = "price-watch-sm"
  lambda_function_arn     = "arn:aws:lambda:eu-west-1:554074174252:function:ingest_data_lambda:$LATEST"
  ecs_cluster_arn         = "arn:aws:ecs:eu-west-1:554074174252:cluster/price-watch-cluster"
  ecs_task_definition_arn = "arn:aws:ecs:eu-west-1:554074174252:task-definition/data-cleaner:4"
  ecs_subnet_ids          = ["subnet-005f72c2eb085579f","subnet-0400225126d8e22c5"]
  ecs_security_group_ids  = ["sg-05bcd2a960ef3bd80"]
  glue_crawler_name       = "crawl_silver_bucket"
}

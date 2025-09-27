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

data "terraform_remote_state" "s3" {
  backend = "local"
  config = {
    path = "../s3/terraform.tfstate"
  }
}
module "price_watch_crawler" {
  source            = "../../modules/glue-crawler"
  crawler_name      = "price-watch-crawler"
  glue_database_name = "price_watch_db"
  s3_target_path    = "s3://${data.terraform_remote_state.s3.outputs.bucket_name}/silver_new/"
  crawler_schedule  = "" # daily at 3 AM UTC
}

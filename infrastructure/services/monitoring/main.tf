module "monitoring" {
  source              = "../../modules/monitoring"
  project_name        = "price-watch"
  lambda_function_name = "ingest_data_lambda"
  ecs_cluster_name     = "price-watch-cluster"
  ecs_service_name     = "data-cleaner-service"
  step_function_arn    = "arn:aws:states:eu-west-1:123456789012:stateMachine:price-watch-sm"
  glue_crawler_name    = "crawl_silver_bucket"
  alert_email          = "youremail@example.com"
}

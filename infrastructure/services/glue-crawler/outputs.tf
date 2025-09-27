output "crawler_name" {
  description = "The name of the Glue crawler"
  value       = module.price_watch_crawler.crawler_name
}

output "database_name" {
  description = "The name of the Glue catalog database"
  value       = module.price_watch_crawler.database_name
}
output "crawler_role_arn" {
  description = "IAM role ARN used by the crawler"
  value       = module.price_watch_crawler.crawler_role_arn
}

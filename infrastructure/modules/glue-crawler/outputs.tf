output "crawler_name" {
  description = "The name of the Glue crawler"
  value       = aws_glue_crawler.crawler.name
}

output "database_name" {
  description = "The name of the Glue catalog database"
  value       = aws_glue_catalog_database.db.name
}

output "crawler_role_arn" {
  description = "IAM role ARN used by the crawler"
  value       = aws_iam_role.crawler_role.arn
}

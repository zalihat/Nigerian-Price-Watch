# resource "aws_glue_catalog_database" "this" {
# #   name = "MyCatalogDatabase"
#     name = var.catalog_database_name
# }
data "aws_caller_identity" "current" {}

# IAM role for the Glue crawler
resource "aws_iam_role" "crawler_role" {
  name               = "${var.crawler_name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Managed Glue role policy
resource "aws_iam_role_policy_attachment" "glue_service_role" {
  role       = aws_iam_role.crawler_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Custom policy for S3 + CloudWatch
resource "aws_iam_policy" "crawler_s3_logs" {
  name        = "${var.crawler_name}-s3-logs"
  description = "Allow Glue crawler to read from S3 and write to CloudWatch logs"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket"
        ]
        Resource = [
          "${replace(var.s3_target_path, "s3://", "arn:aws:s3:::")}",   # bucket ARN
          "${replace(var.s3_target_path, "s3://", "arn:aws:s3:::")}*"   # bucket/* 
        ]
      },
      {
        Effect   = "Allow"
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:${data.aws_caller_identity.current.account_id}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "crawler_s3_logs" {
  role       = aws_iam_role.crawler_role.name
  policy_arn = aws_iam_policy.crawler_s3_logs.arn
}

# Glue Catalog Database
resource "aws_glue_catalog_database" "db" {
  name        = var.glue_database_name
  description = "Glue DB for ${var.crawler_name}"
}

# Glue Crawler
resource "aws_glue_crawler" "crawler" {
  name          = var.crawler_name
  role          = aws_iam_role.crawler_role.arn
  database_name = aws_glue_catalog_database.db.name
  description   = "Crawler for ${var.crawler_name}"

  s3_target {
    path = var.s3_target_path
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

 
  schedule = var.crawler_schedule
 
}

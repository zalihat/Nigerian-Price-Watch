variable "crawler_name" {
  type        = string
  description = "Name of the Glue crawler"
}

variable "glue_database_name" {
  type        = string
  description = "Name of the Glue catalog database"
}

variable "s3_target_path" {
  type        = string
  description = "S3 path the crawler will scan (e.g. s3://my-bucket/prefix/)"
}

variable "crawler_schedule" {
  type        = string
  description = "Optional schedule expression (cron or rate). Leave blank for no schedule."
  default     = ""
}

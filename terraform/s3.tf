# ------------------------------
# S3 Bucket for ingested data
# ------------------------------
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.s3_bucket_name

  lifecycle {
    prevent_destroy = true
  }
}

# ------------------------------
# Upload Glue ETL script to S3
# ------------------------------
resource "aws_s3_object" "clean_data_script" {
  bucket = aws_s3_bucket.data_bucket.bucket
  key    = var.glue_script_key
  source = var.glue_script_source
}

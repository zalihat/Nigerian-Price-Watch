resource "aws_s3_bucket" "data_bucket" {
  bucket = var.s3_bucket_name

  lifecycle {
    prevent_destroy = true
  }
}
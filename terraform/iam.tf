# ------------------------------
# IAM Role for Lambda
# ------------------------------
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "ingest_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}

# Attach basic Lambda execution role (logs)
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach S3 access to Lambda role
resource "aws_iam_role_policy" "lambda_s3" {
  name = "lambda_s3_access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      }
    ]
  })
}

# ------------------------------
# IAM Role for Glue Job
# ------------------------------
# resource "aws_iam_role" "glue_role" {
#   name = "glue-etl-role"

#   assume_role_policy = jsonencode({
#     Version   = "2012-10-17",
#     Statement = [
#       {
#         Effect    = "Allow",
#         Principal = { Service = "glue.amazonaws.com" },
#         Action    = "sts:AssumeRole"
#       }
#     ]
#   })
# }

# # Attach Glue service role policy
# resource "aws_iam_role_policy_attachment" "glue_service_policy" {
#   role       = aws_iam_role.glue_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
# }

# # Attach S3 full access policy to Glue role
# resource "aws_iam_role_policy_attachment" "glue_s3_access" {
#   role       = aws_iam_role.glue_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
# }

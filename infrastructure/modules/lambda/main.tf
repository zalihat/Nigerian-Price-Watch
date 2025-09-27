# -------------------
# IAM Role
# -------------------

# This policy says: "This role can be assumed by Lambda"
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Create the IAM role that the Lambda function will use
resource "aws_iam_role" "this" {
  name               = "${var.function_name}_role"   # role name
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}

# Attach AWS's built-in policy so Lambda can write logs to CloudWatch
resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy: allow Lambda to access the S3 bucket you specify
resource "aws_iam_role_policy" "s3" {
  name = "${var.function_name}_s3"
  role = aws_iam_role.this.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],  # what Lambda can do
        Resource = [
          var.s3_bucket_arn,        # bucket itself
          "${var.s3_bucket_arn}/*"  # all objects inside
        ]
      }
    ]
  })
}

# -------------------
# Lambda Function
# -------------------

# This actually creates the Lambda function in AWS
resource "aws_lambda_function" "this" {
  function_name    = var.function_name   # comes from the service that calls the module
  role             = aws_iam_role.this.arn
  runtime          = var.runtime
  handler          = var.handler
  filename         = var.package_file    # path to your prebuilt ZIP file
  source_code_hash = filebase64sha256(var.package_file) # ensures TF redeploys if ZIP changes
  timeout          = var.timeout

  # Environment variable your Lambda code can use
  environment {
    variables = {
      S3_BUCKET = var.s3_bucket_name
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.basic,
    aws_iam_role_policy.s3
  ]
}

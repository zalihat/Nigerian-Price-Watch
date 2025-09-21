resource "aws_cloudwatch_dashboard" "pipeline" {
  dashboard_name = var.dashboard_name

  dashboard_body = jsonencode({
    widgets = [
      # Lambda Errors
      {
        "type"  : "metric",
        "x"     : 0,
        "y"     : 0,
        "width" : 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["AWS/Lambda", "Errors", "FunctionName", var.lambda_function_name]
          ],
          "stat": "Sum",
          "period": 300,
          "title": "Lambda Errors"
        }
      },
      # ECS CPU Utilization
        {
        "type": "log",
        "x": 12,
        "y": 0,
        "width": 12,
        "height": 6,
        "properties": {
            "query": "fields @timestamp, @message | sort @timestamp desc | limit 20",
            "region": "eu-west-1",
            "title": "ECS Task Logs",
            "logGroupNames": [var.ecs_log_group_name]
  }
}
,
      # Step Function Failures
      {
        "type"  : "metric",
        "x"     : 0,
        "y"     : 6,
        "width" : 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["AWS/States", "ExecutionsFailed", "StateMachineArn", var.step_function_arn]
          ],
          "stat": "Sum",
          "period": 300,
          "title": "Step Function Failures"
        }
      },
      # Glue Crawler Errors
      {
        "type"  : "metric",
        "x"     : 12,
        "y"     : 6,
        "width" : 12,
        "height": 6,
        "properties": {
          "metrics": [
            ["Glue", "CrawlerErrors", "CrawlerName", var.glue_crawler_name]
          ],
          "stat": "Sum",
          "period": 300,
          "title": "Glue Crawler Errors"
        }
      }
    ]
  })
}

# SNS Topic for Alerts
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email # email for notifications
}

# Example Alarm: Lambda Errors > 0
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project_name}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Triggers if Lambda errors occur"
  dimensions = {
    FunctionName = var.lambda_function_name
  }
  alarm_actions = [aws_sns_topic.alerts.arn]
}

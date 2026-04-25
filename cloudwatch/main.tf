terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

# ── SNS Topic ─────────────────────────────────────────────────────────────────

resource "aws_sns_topic" "alerts" {
  name = "real-estate-pipeline-alerts"
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# ── 1. Lambda: Error rate alert ───────────────────────────────────────────────

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "real-estate-lambda-errors"
  alarm_description   = "Lambda validator threw errors"
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions          = { FunctionName = var.lambda_function_name }

  statistic           = "Sum"
  period              = 300        # 5 min window
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

# ── 2. Lambda: Timeout alert ──────────────────────────────────────────────────

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "real-estate-lambda-timeout-risk"
  alarm_description   = "Lambda running close to timeout limit"
  namespace           = "AWS/Lambda"
  metric_name         = "Duration"
  dimensions          = { FunctionName = var.lambda_function_name }

  statistic           = "Maximum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 25000      # alert at 25s (adjust to your timeout - 5s)
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
  unit                = "Milliseconds"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ── 3. Lambda: No invocations (scraper didn't run) ────────────────────────────

resource "aws_cloudwatch_metric_alarm" "lambda_no_invocations" {
  alarm_name          = "real-estate-lambda-not-triggered"
  alarm_description   = "Lambda was not invoked — S3 upload may have failed"
  namespace           = "AWS/Lambda"
  metric_name         = "Invocations"
  dimensions          = { FunctionName = var.lambda_function_name }

  statistic           = "Sum"
  period              = 86400      # 24h — fires if no invocation all day
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "LessThanThreshold"
  treat_missing_data  = "breaching" # missing = bad here

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ── 4. Glue: Job failure alert ────────────────────────────────────────────────

resource "aws_cloudwatch_metric_alarm" "glue_failures" {
  alarm_name          = "real-estate-glue-job-failed"
  alarm_description   = "Glue ETL job (bronze → silver) failed"
  namespace           = "Glue"
  metric_name         = "glue.driver.aggregate.numFailedTasks"
  dimensions          = { JobName = var.glue_job_name }

  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ── 5. Glue: Job didn't run (custom metric via log filter) ───────────────────

resource "aws_cloudwatch_log_metric_filter" "glue_success" {
  name           = "glue-job-succeeded"
  log_group_name = "/aws-glue/jobs/output"
  pattern        = "Job succeeded"

  metric_transformation {
    name      = "GlueJobSuccess"
    namespace = "RealEstatePipeline"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "glue_no_run" {
  alarm_name          = "real-estate-glue-job-not-run"
  alarm_description   = "Glue ETL job did not complete successfully today"
  namespace           = "RealEstatePipeline"
  metric_name         = "GlueJobSuccess"

  statistic           = "Sum"
  period              = 86400
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "LessThanThreshold"
  treat_missing_data  = "breaching"

  alarm_actions = [aws_sns_topic.alerts.arn]
}

# ── 6. S3: Create the log group first, then filter it ────────────────────────

resource "aws_cloudwatch_log_group" "scraper" {
  name              = "/real-estate/scraper"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_metric_filter" "s3_upload" {
  name           = "s3-scraper-upload"
  log_group_name = aws_cloudwatch_log_group.scraper.name  # depends on group above
  pattern        = "Uploaded"

  metric_transformation {
    name          = "ScraperUploadCount"
    namespace     = "RealEstatePipeline"
    value         = "1"
    default_value = "0"
  }
}

# ── Dashboard (fixed: added region to every widget) ───────────────────────────

resource "aws_cloudwatch_dashboard" "pipeline" {
  dashboard_name = "RealEstatePipeline"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric", x = 0, y = 0, width = 8, height = 6,
        properties = {
          title   = "Lambda Errors"
          region  = var.aws_region
          metrics = [["AWS/Lambda", "Errors", "FunctionName", var.lambda_function_name]]
          period  = 300, stat = "Sum", view = "timeSeries"
        }
      },
      {
        type = "metric", x = 8, y = 0, width = 8, height = 6,
        properties = {
          title   = "Lambda Duration"
          region  = var.aws_region
          metrics = [["AWS/Lambda", "Duration", "FunctionName", var.lambda_function_name]]
          period  = 300, stat = "Maximum", view = "timeSeries"
        }
      },
      {
        type = "metric", x = 16, y = 0, width = 8, height = 6,
        properties = {
          title   = "Lambda Invocations"
          region  = var.aws_region
          metrics = [["AWS/Lambda", "Invocations", "FunctionName", var.lambda_function_name]]
          period  = 300, stat = "Sum", view = "timeSeries"
        }
      },
      {
        type = "metric", x = 0, y = 6, width = 12, height = 6,
        properties = {
          title   = "Scraper Uploads / day"
          region  = var.aws_region
          metrics = [["RealEstatePipeline", "ScraperUploadCount"]]
          period  = 86400, stat = "Sum", view = "timeSeries"
        }
      },
      {
        type = "metric", x = 12, y = 6, width = 12, height = 6,
        properties = {
          title   = "Glue Job Success / day"
          region  = var.aws_region
          metrics = [["RealEstatePipeline", "GlueJobSuccess"]]
          period  = 86400, stat = "Sum", view = "timeSeries"
        }
      }
    ]
  })
}
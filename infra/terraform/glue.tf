resource "aws_glue_job" "bronze_to_silver" {
  name     = "${var.project_name}-bronze-to-silver"
  role_arn = aws_iam_role.glue_role.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.glue_scripts.bucket}/scripts/bronze_to_silver.py"
    python_version  = "3"
  }

  default_arguments = {
    "--SOURCE_BUCKET"      = aws_s3_bucket.bronze.bucket
    "--TARGET_BUCKET"      = aws_s3_bucket.silver.bucket
    "--SOURCE_PREFIX"      = "raw/"
    "--TARGET_PREFIX"      = "cleaned/"
    "--job-language"       = "python"
    "--enable-metrics"     = "true"
    "--enable-auto-scaling" = "true"
  }

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2

  timeout = 60

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
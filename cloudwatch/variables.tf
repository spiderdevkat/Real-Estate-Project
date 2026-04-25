variable "alert_email" {
  description = "devender20025090@gmail.com"
  type        = string
}

variable "lambda_function_name" {
  description = "realestate-data-validator"
  type        = string
  default     = "real-estate-validator"
}

variable "glue_job_name" {
  description = "realestate-tracker-bronze-to-silver"
  type        = string
  default     = "real-estate-bronze-to-silver"
}

variable "s3_bucket_name" {
  description = "realestate-tracker-bronze-dev"
  type        = string
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
resource "aws_s3_bucket" "bronze" {
  bucket = "realestate-tracker-bronze-dev"

  tags = {
    Project     = "realestate-tracker"
    Layer       = "bronze"
    Environment = "dev"
  }
}

resource "aws_s3_bucket" "silver" {
  bucket = "realestate-tracker-silver-dev"

  tags = {
    Project     = "realestate-tracker"
    Layer       = "silver"
    Environment = "dev"
  }
}

resource "aws_s3_bucket" "gold" {
  bucket = "realestate-tracker-gold-dev"

  tags = {
    Project     = "realestate-tracker"
    Layer       = "gold"
    Environment = "dev"
  }
}

# Glue scripts bucket
resource "aws_s3_bucket" "glue_scripts" {
  bucket = "${var.project_name}-scripts-dev"

  tags = {
    Project     = var.project_name
    Layer       = "scripts"
    Environment = var.environment
  }
}
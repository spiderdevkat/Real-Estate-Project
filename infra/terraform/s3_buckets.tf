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
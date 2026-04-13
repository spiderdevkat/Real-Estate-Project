# IAM Role for Glue
resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Attach AWS managed Glue policy
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Custom policy for S3 access
resource "aws_iam_role_policy" "glue_s3_policy" {
  name = "${var.project_name}-glue-s3-policy"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::realestate-tracker-bronze-dev",
          "arn:aws:s3:::realestate-tracker-bronze-dev/*",
          "arn:aws:s3:::realestate-tracker-silver-dev",
          "arn:aws:s3:::realestate-tracker-silver-dev/*",
          "arn:aws:s3:::realestate-tracker-gold-dev",
          "arn:aws:s3:::realestate-tracker-gold-dev/*",
          "arn:aws:s3:::${var.project_name}-scripts-dev",
          "arn:aws:s3:::${var.project_name}-scripts-dev/*"
        ]
      }
    ]
  })
}
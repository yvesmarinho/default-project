terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Remote state backend — configure before first `terraform init`
  # Uncomment and fill in your S3 bucket and DynamoDB table names.
  #
  # backend "s3" {
  #   bucket         = "my-company-terraform-state"
  #   key            = "my-project/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "my-company-terraform-lock"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      env        = var.env
      product    = var.project_name
      managed-by = "terraform"
    }
  }
}

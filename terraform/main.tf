terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.62.0"
    }
  }

}

provider "aws" {
  region = var.aws_region
}

# --- Data Source for AWS Caller Identity ---
# Used to get the AWS account ID for constructing ARNs.
data "aws_caller_identity" "current" {}
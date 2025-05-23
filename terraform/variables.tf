

variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "A unique name for your CodeBuild project and associated resources."
  type        = string
  default     = "StreamingExplorer"
}

variable "github_repo_url" {
  description = "The HTTPS URL of your GitHub repository"
  type        = string
  default     = "https://github.com/OmarHexa/Streaming_explorer.git"
}

variable "ecr_repo_prefix" {
  description = "A prefix for ECR repository names"
  type        = string
  default     = "streaming-explorer"
}
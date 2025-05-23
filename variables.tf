

variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "eu-central-1" # Change to your desired region
}

variable "project_name" {
  description = "A unique name for your CodeBuild project and associated resources."
  type        = string
  default     = "StreamingExplorer" # Customize this name
}

variable "github_repo_url" {
  description = "The HTTPS URL of your GitHub repository"
  type        = string
  # IMPORTANT: Replace with your actual GitHub repository URL
  default     = "https://github.com/OmarHexa/Streaming_explorer.git"
}

variable "ecr_repo_name" {
  description = "The name for your ECR repository."
  type        = string
  default     = "omar/streamingexplorer" # Customize this name
}
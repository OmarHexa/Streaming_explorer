
provider "aws" {
  region = "your_aws_region"
}

resource "aws_ecr_repository" "backend" {
  name = "backend-repository"
}

resource "aws_ecr_repository" "frontend" {
  name = "frontend-repository"
}

# Use this data source to obtain the AWS ECR login command
data "aws_ecr_authorization_token" "ecr_auth" {}

# Build the backend Docker image and push it to AWS ECR
resource "null_resource" "build_and_push_backend" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<-EOT
      eval $(${data.aws_ecr_authorization_token.ecr_auth.authorization_token})
      docker build -t ${aws_ecr_repository.backend.repository_url}:latest ./backend
      docker push ${aws_ecr_repository.backend.repository_url}:latest
    EOT
  }
}

# Build the frontend Docker image and push it to AWS ECR
resource "null_resource" "build_and_push_frontend" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<-EOT
      eval $(${data.aws_ecr_authorization_token.ecr_auth.authorization_token})
      docker build -t ${aws_ecr_repository.frontend.repository_url}:latest ./frontend
      docker push ${aws_ecr_repository.frontend.repository_url}:latest
    EOT
  }
}

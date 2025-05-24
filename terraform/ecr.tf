# --- AWS ECR Repository for Backend ---
resource "aws_ecr_repository" "backend_ecr_repo" {
  name                 = "${var.ecr_repo_prefix}-backend-repo" # Example: my-docker-app-backend-repo
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.project_name}-backend-ecr-repo"
    Environment = "Dev"
  }
}

# --- AWS ECR Repository for Frontend ---
resource "aws_ecr_repository" "frontend_ecr_repo" {
  name                 = "${var.ecr_repo_prefix}-frontend-repo" # Example: my-docker-app-frontend-repo
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "${var.project_name}-frontend-ecr-repo"
    Environment = "Dev"
  }
}
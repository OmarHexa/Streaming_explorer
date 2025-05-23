

# --- Data Source for AWS Caller Identity ---
# Used to get the AWS account ID for constructing ARNs.
data "aws_caller_identity" "current" {}

# --- CloudWatch Log Group (optional but safer to declare) ---
resource "aws_cloudwatch_log_group" "codebuild_logs" {
  name = "/aws/codebuild/${var.project_name}-project"
}


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
# --- IAM Role for CodeBuild ---
# CodeBuild needs an IAM role to perform actions like reading from S3,
# pushing to ECR, and writing logs to CloudWatch.
resource "aws_iam_role" "codebuild_role" {
  name = "${var.project_name}-codebuild-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-codebuild-role"
    Environment = "Dev"
  }
}


# --- AWS CodeBuild Project ---
# This is the core resource that defines your build process.
resource "aws_codebuild_project" "app_codebuild_project" {
  name          = "${var.project_name}-project"
  description   = "CodeBuild project to build and push Docker image to ECR"
  service_role  = aws_iam_role.codebuild_role.arn
  build_timeout = "15" # Build timeout in minutes

  # Source configuration (GitHub)
  source {
    type            = "GITHUB"
    location        = var.github_repo_url
    git_clone_depth = 1 # Clone only the latest commit
    # For private repositories, you would typically need to set up a CodeStar connection
    # or use OAuth credentials. For simplicity, this assumes a public repo or pre-configured connection.
    # If using a CodeStar connection:
    # report_build_status = true # Reports build status back to GitHub
  }

  # Artifacts configuration (where build output goes)
  artifacts {
    type = "NO_ARTIFACTS" # We are pushing to ECR, so no artifacts are needed in S3 for the build output.
  }

  # Environment configuration (build environment details)
  environment {
    compute_type                = "BUILD_GENERAL1_SMALL" # Or MEDIUM, LARGE
    image                       = "aws/codebuild/standard:5.0" # Use a standard image with Docker support
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true # Required for Docker builds

    # Environment variables passed to the build environment
    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }
    environment_variable {
      name  = "AWS_DEFAULT_REGION"
      value = var.aws_region
    }
    environment_variable {
      name  = "BACKEND_ECR_REPOSITORY_URI"
      value = aws_ecr_repository.backend_ecr_repo.repository_url
    }
    environment_variable {
      name  = "FRONTEND_ECR_REPOSITORY_URI"
      value = aws_ecr_repository.frontend_ecr_repo.repository_url
    }
    environment_variable {
      name  = "IMAGE_TAG"
      value = "latest" # Or use a dynamic value like CODEBUILD_RESOLVED_SOURCE_VERSION in buildspec
    }
  }

  # Logs configuration (where build logs go)
  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/${var.project_name}"
      stream_name = "build-log-stream"
      status      = "ENABLED"
    }
  }

  tags = {
    Name        = "${var.project_name}-codebuild-project"
    Environment = "Dev"
  }
}



# --- IAM Policy for CodeBuild Role ---
resource "aws_iam_role_policy" "codebuild_policy" {
  name = "${var.project_name}-inline-policy"
  role = aws_iam_role.codebuild_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Resource = [
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/codebuild/${var.project_name}",
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/codebuild/${var.project_name}:*"
        ],
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
      },
      {
        Effect = "Allow",
        Resource = [
          aws_ecr_repository.backend_ecr_repo.arn, # NEW
          aws_ecr_repository.frontend_ecr_repo.arn  # NEW
          # If you had the original ecr_repo, remove or update it if you are consolidating
        ]
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:CompleteLayerUpload",
          "ecr:InitiateLayerUpload",
          "ecr:PutImage",
          "ecr:UploadLayerPart"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:GetBucketAcl",
          "s3:GetBucketLocation"
        ],
        Resource = "arn:aws:s3:::codepipeline-${var.aws_region}-*"
      },
      {
        Effect = "Allow",
        Action = [
          "codebuild:CreateReportGroup",
          "codebuild:CreateReport",
          "codebuild:UpdateReport",
          "codebuild:BatchPutTestCases",
          "codebuild:BatchPutCodeCoverages"
        ],
        Resource = "arn:aws:codebuild:${var.aws_region}:${data.aws_caller_identity.current.account_id}:report-group/${var.project_name}-*"
      },
      {
        Sid: "SecretsManagerAccess",
        Effect = "Allow",
        Action = "secretsmanager:GetSecretValue",
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:github_token-*"
      },
      {
        Sid: "GitHubAccess",
        Effect = "Allow",
        Action = [
          "codestar:*",
          "codestar-connections:*"
        ],
        Resource = "*"
      }
    ]
  })
}

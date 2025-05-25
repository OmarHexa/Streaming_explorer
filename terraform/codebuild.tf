
# --- AWS CodeBuild Project ---
# This is the core resource that defines your build process.
resource "aws_codebuild_project" "app_codebuild_project" {
  name          = "${var.project_name}-project"
  description   = "CodeBuild project to build and push Docker image to ECR"
  service_role  = aws_iam_role.codebuild_role.arn
  build_timeout = "10" # Build timeout in minutes

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
    type = "S3"
    location = aws_s3_bucket.codedeploy_artifacts_bucket.id
    name = "${var.project_name}-build"
    packaging = "ZIP"
    namespace_type = "BUILD_ID"
    path = "artifacts"
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
        Resource = "*",
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
        Effect = "Allow",
        Action = "secretsmanager:GetSecretValue",
        Resource = "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:github_token-*"
      },
      {
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

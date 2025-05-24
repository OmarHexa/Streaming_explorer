# --- IAM Role for CodeDeploy Service ---
# This role allows CodeDeploy to interact with other AWS services on your behalf.
resource "aws_iam_role" "codedeploy_service_role" {
  name = "${var.project_name}-codedeploy-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "codedeploy.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-codedeploy-service-role"
    Environment = "Dev"
  }
}

# --- IAM Policy Attachment for CodeDeploy Service Role ---
# Attach the standard AWSCodeDeployRole managed policy.
resource "aws_iam_role_policy_attachment" "codedeploy_managed_policy" {
  role       = aws_iam_role.codedeploy_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole" # Standard CodeDeploy managed policy
}

# --- CodeDeploy Application ---
# A logical entity that represents the application you want to deploy.
resource "aws_codedeploy_application" "app_application" {
  name = "${var.project_name}-application"

  tags = {
    Name        = "${var.project_name}-application"
    Environment = "Dev"
  }
}

# --- CodeDeploy Deployment Group ---
# Defines the set of EC2 instances to deploy to and the deployment configuration.
resource "aws_codedeploy_deployment_group" "app_deployment_group" {
  app_name               = aws_codedeploy_application.app_application.name
  deployment_group_name  = "${var.project_name}-deployment-group"
  service_role_arn       = aws_iam_role.codedeploy_service_role.arn
  deployment_config_name = "CodeDeployDefault.OneAtATime" # Or CodeDeployDefault.AllAtOnce for faster but less safe deployments

  # Target instances using the EC2 tag we applied to the EC2 instance
  ec2_tag_set {
    ec2_tag_filter {
      key   = "CodeDeployGroup"
      type  = "KEY_AND_VALUE"
      value = "${var.project_name}-deployment-group"
    }
  }

  # Configure deployment style (e.g., in-place, blue/green)
  deployment_style {
    deployment_option = "IN_PLACE" # Deploy directly onto the existing instances
    deployment_type   = "ONE_AT_A_TIME" # Deploy to one instance at a time
  }

  # Automatic rollback on deployment failure
  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE"]
  }

  tags = {
    Name        = "${var.project_name}-deployment-group"
    Environment = "Dev"
  }
}

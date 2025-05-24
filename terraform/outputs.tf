
output "backend_ecr_repository_uri" {
  description = "The URI of the backend ECR repository."
  value       = aws_ecr_repository.backend_ecr_repo.repository_url
}

output "frontend_ecr_repository_uri" {
  description = "The URI of the frontend ECR repository."
  value       = aws_ecr_repository.frontend_ecr_repo.repository_url
}

output "codebuild_project_name" {
  description = "The name of the AWS CodeBuild project."
  value       = aws_codebuild_project.app_codebuild_project.name
}

output "codebuild_project_arn" {
  description = "The ARN of the AWS CodeBuild project."
  value       = aws_codebuild_project.app_codebuild_project.arn
}

output "codedeploy_application_name" {
  description = "The name of the CodeDeploy application."
  value       = aws_codedeploy_application.app_application.name
}

output "codedeploy_deployment_group_name" {
  description = "The name of the CodeDeploy deployment group."
  value       = aws_codedeploy_deployment_group.app_deployment_group.deployment_group_name
}

output "ec2_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.app_server.public_ip
}

output "ec2_public_dns" {
  description = "The public DNS name of the EC2 instance."
  value       = aws_instance.app_server.public_dns
}


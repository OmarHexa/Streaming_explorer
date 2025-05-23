output "public_ip" {
    value = aws_instance.backend.public_ip
    }

output "ecr_repository_uri" {
  description = "The URI of the ECR repository."
  value       = aws_ecr_repository.app_ecr_repo.repository_url
}

output "codebuild_project_name" {
  description = "The name of the AWS CodeBuild project."
  value       = aws_codebuild_project.app_codebuild_project.name
}

output "codebuild_project_arn" {
  description = "The ARN of the AWS CodeBuild project."
  value       = aws_codebuild_project.app_codebuild_project.arn
}

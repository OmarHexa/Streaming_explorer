# output "public_ip" {
#     value = aws_instance.backend.public_ip
#     }

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

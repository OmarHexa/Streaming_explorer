# --- CloudWatch Log Group (optional but safer to declare) ---
resource "aws_cloudwatch_log_group" "codebuild_logs" {
  name = "/aws/codebuild/${var.project_name}-project"
}

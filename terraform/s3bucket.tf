# --- S3 Bucket for CodeDeploy Artifacts ---
# This bucket will store the deployment artifacts (zip file) that CodeDeploy will use.
resource "aws_s3_bucket" "codedeploy_artifacts_bucket" {
  bucket = var.code_deploy_bucket_name
  tags = {
    Name        = "${var.project_name}-codedeploy-artifacts"
    Environment = "Dev"
  }
}
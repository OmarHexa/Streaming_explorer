#!/bin/bash
echo "--- CodeDeploy Hook: ApplicationStart - Starting Docker Compose application ---"

DEPLOY_DIR="/home/ec2-user/streaming-explorer"
cd $DEPLOY_DIR || { echo "Error: Deployment directory not found at $DEPLOY_DIR"; exit 1; }

echo "Getting ECR login password and logging in to Docker..."
# Fetch AWS account ID and region dynamically from instance metadata
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_DEFAULT_REGION=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | grep region | awk -F\" '{print $4}')

# Log in to ECR
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com || { echo "ECR login failed!"; exit 1; }

# IMPORTANT: Ensure your docker-compose.yaml references the ECR images with full URIs
# Example: image: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/streaming-explorer-backend-repo:${IMAGE_TAG}
# If your docker-compose.yaml uses environment variables like ${AWS_ACCOUNT_ID},
# you need to ensure these are set in the shell before docker-compose up.
# CodeDeploy passes environment variables from the buildspec.yaml to the instance,
# but for docker-compose, it's often easier to define them directly in the .env file
# or substitute them into the docker-compose.yaml before running.
# For simplicity, we assume the .env file (copied in AfterInstall) handles DB credentials,
# and the ECR images are referenced with full URIs or variables that docker-compose can resolve.

echo "Starting Docker Compose application in detached mode..."
docker-compose -f docker-compose.aws.yaml up -d || { echo "Docker Compose failed to start!"; exit 1; }

echo "Application started."

#!/bin/bash
echo "--- CodeDeploy Hook: AfterInstall - Copying .env file and Nginx certificates ---"

DEPLOY_DIR="/home/ec2-user/streaming-explorer"
cd $DEPLOY_DIR || { echo "Error: Deployment directory not found at $DEPLOY_DIR"; exit 1; }

# Ensure the Nginx certificate directory exists in the target location
mkdir -p $DEPLOY_DIR/nginx/certificate

# Copy .env file
# IMPORTANT: For production, do NOT commit sensitive .env files to Git.
# Instead, retrieve variables from AWS Secrets Manager or Parameter Store here.
# For this example, we assume `.env.example` is in your repo and will be used as `.env`.
echo "Copying .env.example to .env..."
cp $DEPLOY_DIR/.env.example $DEPLOY_DIR/.env || { echo "Error copying .env.example"; exit 1; }

# Copy Nginx configuration
echo "Copying Nginx configuration..."
cp $DEPLOY_DIR/nginx/nginx.conf $DEPLOY_DIR/nginx/nginx.conf || { echo "Error copying nginx.conf"; exit 1; }

# Copy SSL certificates
echo "Copying Nginx SSL certificates..."
# Ensure your certificates are correctly placed in your repository under nginx/certificate/
cp $DEPLOY_DIR/nginx/certificate/* $DEPLOY_DIR/nginx/certificate/ || { echo "Error copying Nginx certificates"; exit 1; }

# Copy database initialization scripts/Dockerfile
echo "Copying database initialization files..."
mkdir -p $DEPLOY_DIR/src/init # Create directory if it doesn't exist
cp -r $DEPLOY_DIR/src/init/* $DEPLOY_DIR/src/init/ || { echo "Error copying database init files"; exit 1; }


echo "Files copied successfully."

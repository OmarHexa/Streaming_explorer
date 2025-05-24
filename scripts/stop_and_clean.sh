#!/bin/bash
echo "--- CodeDeploy Hook: BeforeInstall - Stopping existing Docker containers and cleaning up ---"

DEPLOY_DIR="/home/ec2-user/streaming-explorer"
cd $DEPLOY_DIR || { echo "Error: Deployment directory not found at $DEPLOY_DIR"; exit 1; }

echo "Stopping and removing existing Docker containers..."
# `docker-compose down` stops and removes containers, networks, and volumes defined in the compose file.
# `|| true` prevents the script from failing if containers don't exist (e.g., first deployment).
docker-compose down || true

echo "Removing old Docker images (optional, but good for disk space)..."
# Remove all dangling images (images not associated with a container)
docker image prune -f || true
# Alternatively, remove all images (use with caution)
# docker rmi $(docker images -aq) || true

echo "Cleanup complete."

#!/bin/bash
echo "Starting user data script..."
apt-get update -y
apt-get install -y docker.io git ruby wget curl

# Start Docker
systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

# Install Docker Compose
DOCKER_COMPOSE_VERSION=2.23.3
curl -L "https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install CodeDeploy Agent
cd /tmp
wget https://aws-codedeploy-${aws_region}.s3.${aws_region}.amazonaws.com/latest/install
chmod +x ./install
./install auto
systemctl enable codedeploy-agent
systemctl start codedeploy-agent

echo "User data script finished."

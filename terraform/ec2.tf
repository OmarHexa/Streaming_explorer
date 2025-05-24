# --- AWS ami for Ubuntu 24.04 ---
# This data source fetches the most recent Ubuntu 24.04 AMI for use in EC2 instances.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-20250305"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

}

# --- EC2 Instance for Streaming Explorer ---
# This resource creates an EC2 instance for the Streaming Explorer application.
resource "aws_instance" "streamingexplorer" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  associate_public_ip_address = true
  key_name = aws_key_pair.backend.key_name
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  subnet_id = aws_subnet.app_subnet.id
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
  # User data script to install Docker, Docker Compose, and CodeDeploy Agent on first boot.
  user_data = <<-EOF
              #!/bin/bash
              echo "Starting user data script..."
              # Update all installed packages
              yum update -y

              # Install Docker and Git
              echo "Installing Docker and Git..."
              yum install -y docker git
              service docker start
              usermod -a -G docker ec2-user # Add ec2-user to the docker group so it can run docker commands without sudo

              # Install Docker Compose
              echo "Installing Docker Compose..."
              curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose

              # Install CodeDeploy Agent
              echo "Installing CodeDeploy Agent..."
              yum install -y ruby # Ruby is a dependency for the CodeDeploy agent installer
              wget https://aws-codedeploy-${var.aws_region}.s3.${var.aws_region}.amazonaws.com/latest/install -O /tmp/install
              chmod +x /tmp/install
              /tmp/install auto # Install and start the agent, configure it to start on boot
              service codedeploy-agent start
              chkconfig codedeploy-agent on

              echo "User data script finished."
              EOF

  tags = {
    Name        = "${var.project_name}-app-server"
    Environment = "Dev"
    # This tag is used by CodeDeploy to identify target instances for deployment
    CodeDeployGroup = "${var.project_name}-deployment-group"
  }

  
}


# --- IAM Role for EC2 Instance (for SSM, ECR Pull, CloudWatch Logs) ---
# This role allows the EC2 instance to perform necessary actions.
resource "aws_iam_role" "ec2_instance_role" {
  name = "${var.project_name}-ec2-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-ec2-instance-role"
    Environment = "Dev"
  }
}


# --- IAM Policy Attachments for EC2 Instance Role ---
# Attach the AmazonSSMManagedInstanceCore policy for CodeDeploy agent and SSM access.
resource "aws_iam_role_policy_attachment" "ec2_ssm_policy" {
  role       = aws_iam_role.ec2_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore" # Allows SSM agent to manage the instance
}



# Custom policy for EC2: ECR pull, CloudWatch logs, S3 access for CodeDeploy artifacts
resource "aws_iam_role_policy" "ec2_custom_policy" {
  name = "${var.project_name}-ec2-custom-policy"
  role = aws_iam_role.ec2_instance_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetAuthorizationToken" # Needed for docker login to ECR on the EC2 instance
        ]
        Resource = "*" # ECR GetAuthorizationToken requires * resource
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:*" # Allow logging to any log group
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.codedeploy_artifacts_bucket.arn,
          "${aws_s3_bucket.codedeploy_artifacts_bucket.arn}/*"
        ]
      }
    ]
  })
}

# --- EC2 Instance Profile ---
# An instance profile is a container for an IAM role that you can use to pass role information to an EC2 instance.
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${var.project_name}-ec2-instance-profile"
  role = aws_iam_role.ec2_instance_role.name
}

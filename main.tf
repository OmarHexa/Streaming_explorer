provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "fastapi_server" {
  ami           = "ami-0123456789abcdef0"  # Specify the AMI ID for your desired Amazon Machine Image
  instance_type = "t2.micro"               # Specify the instance type, e.g., t2.micro
  key_name      = "fastapiserver_key"     # Specify the key pair name for SSH access
  # subnet_id     = "subnet-0123456789abcdef0"  # Specify the subnet ID where the instance will be launched

  tags = {
    Name = "FastAPI Server"
  }
}

resource "aws_instance" "streamlit_server" {
  ami           = "ami-0123456789abcdef0"  # Specify the AMI ID for your desired Amazon Machine Image
  instance_type = "t2.micro"               # Specify the instance type, e.g., t2.micro
  key_name      = "streamlitserver_key"     # Specify the key pair name for SSH access
  # subnet_id     = "subnet-0123456789abcdef0"  # Specify the subnet ID where the instance will be launched

  tags = {
    Name = "Streamlit Server"
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "fastapi_server" {
  ami           = "ami-0123456789abcdef0"  # Replace with the actual AMI ID
  instance_type = "t2.micro"
  key_name      = "your-key-pair-name"
  subnet_id     = "subnet-0123456789abcdef0"
  tags = {
    Name = "FastAPI Server"
  }
}

resource "aws_db_instance" "mysql_instance" {
  identifier           = "my-mysql-db"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "8.0.21"
  instance_class       = "db.t2.micro"
  username             = "db_user"
  password             = "db_password"
  parameter_group_name = "default.mysql8.0"
  publicly_accessible  = false
  multi_az             = false
  skip_final_snapshot  = true

  vpc_security_group_ids = [aws_security_group.mysql_sg.id]


  tags = {
    Name = "My MySQL Database"
  }
}

resource "aws_security_group" "mysql_sg" {
  name        = "mysql_sg"
  description = "Security group for MySQL RDS instance"

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

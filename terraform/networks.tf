
# --- AWS VPC and Networking Configuration ---
resource "aws_vpc" "app_vpc" {
  cidr_block = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  
}

# --- Subnet Configuration ---
resource "aws_subnet" "app_subnet" {
  vpc_id            = aws_vpc.app_vpc.id
  cidr_block        = cidrsubnet(aws_vpc.app_vpc.cidr_block, 3, 1)
  availability_zone = "eu-central-1"
}

# --- Internet Gateway Configuration ---
resource "aws_internet_gateway" "app_gateway" {
    vpc_id = aws_vpc.app_vpc.id
}

# --- Route Table Configuration ---
# This route table allows all traffic to go through the Internet Gateway
resource "aws_route_table" "app_route_table" {
    vpc_id = aws_vpc.app_vpc.id
    
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.app_gateway.id
    }

  
}

# --- Route Table Association ---
# This associates the route table with the subnet, allowing traffic to flow
# from the subnet to the Internet Gateway
resource "aws_route_table_association" "app_table_association" {
    subnet_id      = aws_subnet.app_subnet.id
    route_table_id = aws_route_table.app_route_table.id
}

# --- Security Group Configuration ---
# This security group allows all inbound traffic on port 22 (SSH) and all outbound traffic
resource "aws_security_group" "app_sg" {
    name = "allow-all"
  vpc_id = aws_vpc.app_vpc.id

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
  }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = -1
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# --- Key Pair Configuration ---
# This key pair is used to SSH into the EC2 instance
resource "aws_key_pair" "backend" {
  key_name = "my-key-pair"
  public_key = file("~/.ssh/my-ec2-key.pub")
}

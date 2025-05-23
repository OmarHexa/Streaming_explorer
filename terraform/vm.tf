
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


resource "aws_vpc" "backend" {
  cidr_block = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  
}

resource "aws_subnet" "backend" {
  vpc_id            = aws_vpc.backend.id
  cidr_block        = cidrsubnet(aws_vpc.backend.cidr_block, 3, 1)
  availability_zone = "eu-central-1a"
}

resource "aws_internet_gateway" "backend" {
    vpc_id = aws_vpc.backend.id
}

resource "aws_route_table" "backend" {
    vpc_id = aws_vpc.backend.id
    
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.backend.id
    }

  
}

resource "aws_route_table_association" "backend" {
    subnet_id      = aws_subnet.backend.id
    route_table_id = aws_route_table.backend.id
}

resource "aws_security_group" "backend" {
    name = "allow-all"
  vpc_id = aws_vpc.backend.id

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

resource "aws_key_pair" "backend" {
  key_name = "my-key-pair"
  public_key = file("~/.ssh/my-ec2-key.pub")
}


resource "aws_instance" "backend" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  associate_public_ip_address = true
  key_name = aws_key_pair.backend.key_name
  vpc_security_group_ids = [aws_security_group.backend.id]
  subnet_id = aws_subnet.backend.id
  
  
}
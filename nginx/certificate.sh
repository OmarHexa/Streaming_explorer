#!/bin/bash

# Create directory for certificates
CERT_DIR="nginx/certificate"
mkdir -p "$CERT_DIR"

# File paths
CRT_FILE="$CERT_DIR/nginx-selfsigned.crt"
KEY_FILE="$CERT_DIR/nginx-selfsigned.key"

# Generate self-signed certificate
echo "Generating self-signed certificate..."
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout "$KEY_FILE" \
  -out "$CRT_FILE" \
  -subj "/C=DE/ST=Saxony/L=Dresden/O=MyOrg/CN=localhost"

echo "Certificate and key have been created:"
echo " - Certificate: $CRT_FILE"
echo " - Key:         $KEY_FILE"

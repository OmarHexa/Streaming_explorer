#!/bin/bash
echo "--- CodeDeploy Hook: ValidateService - Validating service health ---"

# Give the application some time to fully start up and become ready
sleep 60 # Increased sleep to allow all services (especially DB) to initialize

echo "Performing health checks..."

# Health check for Nginx (frontend access)
echo "Checking Nginx (frontend) health on localhost:80..."
if ! curl -f http://localhost:80; then
  echo "Nginx health check failed! Application might not be accessible."
  exit 1
fi
echo "Nginx (frontend) health check passed."

# Optional: Add more specific health checks for backend and frontend if they have dedicated endpoints
# Example for backend (assuming it listens on port 8000 internally):
# echo "Checking Backend health on localhost:8000/health..."
# if ! curl -f http://localhost:8000/health; then
#   echo "Backend health check failed!"
#   exit 1
# fi
# echo "Backend health check passed."
# Example for frontend (if it has a separate internal port, e.g., 8501, and you want to check it directly)
# echo "Checking Frontend health on localhost:8501..."
# if ! curl -f http://localhost:8501; then
#   echo "Frontend health check failed!"
#   exit 1
# fi
# echo "Frontend health check passed."

echo "Service validation successful."
exit 0
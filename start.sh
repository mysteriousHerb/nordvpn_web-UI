#!/bin/bash

# Source the .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start the FastAPI server
echo "Starting FastAPI server..."
pipenv run uvicorn api:app --host 0.0.0.0 --port ${NORDVPN_UI_PORT:-8000} --reload &

# Wait for the server to start (adjust sleep time if needed)
sleep 5

# Print access links
echo "Access the API Swagger UI at: http://localhost:${NORDVPN_UI_PORT:-8000}/docs"
echo "Access the Web UI at: http://localhost:${NORDVPN_UI_PORT:-8000}/static/index.html"

# # Keep the script running
# wait
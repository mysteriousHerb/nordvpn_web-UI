#!/bin/bash

# Start the FastAPI server
echo "Starting FastAPI server..."
pipenv run uvicorn api:app --host 0.0.0.0 --port 8000 &

# Wait for the FastAPI server to start
sleep 5

# Start the Streamlit UI
echo "Starting Streamlit UI..."
pipenv run streamlit run ui.py &

# Wait for both processes to start
wait

# Print access links
echo "Access the API Swagger UI at: http://localhost:8000/docs"
echo "Access the Streamlit UI at: http://localhost:8501"

# Keep the script running
wait

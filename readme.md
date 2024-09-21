# NordVPN Control Panel

This project provides a user-friendly interface to control NordVPN using a FastAPI backend and a Streamlit frontend.

## Project Structure

- `api.py`: FastAPI backend that interfaces with NordVPN CLI
- `ui.py`: Streamlit frontend for user interaction
- `start.sh`: Shell script to start both the backend and frontend
- `Pipfile`: Python dependencies management

## Setup

1. Ensure you have Python 3.10 installed.
2. Install pipenv: `pip install pipenv`
3. Install dependencies: `pipenv install`

## Running the Application

1. Make sure NordVPN CLI is installed and configured on your system.
2. Run the start script: `./start.sh`

The script will start both the FastAPI backend and the Streamlit frontend.

- API Swagger UI: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501

## Features

- View NordVPN connection status
- Connect to specific countries (with priority countries highlighted)
- Disconnect from VPN
- View and modify NordVPN settings
- Select VPN technology (NordLynx or OpenVPN)
- Choose VPN protocol (TCP or UDP)

## API Endpoints

- GET `/status`: Retrieve current VPN status
- GET `/countries`: Get list of available countries
- POST `/connect/{country}`: Connect to a specific country
- GET `/technologies`: List available VPN technologies
- GET `/protocols`: List available VPN protocols
- POST `/set/{setting}/{value}`: Modify a NordVPN setting
- GET `/settings`: Retrieve current NordVPN settings
- POST `/disconnect`: Disconnect from VPN

## Note

Ensure that you have the necessary permissions to run NordVPN commands on your system.

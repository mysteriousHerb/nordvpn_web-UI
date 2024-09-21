# NordVPN Control Panel

This project provides a user-friendly interface to control NordVPN using a FastAPI backend and a static HTML/Vue.js frontend.

## Project Structure

- `api.py`: FastAPI backend that interfaces with NordVPN CLI
- `static/index.html`: Static HTML file with Vue.js for user interaction
- `start.sh`: Shell script to start the backend
- `Pipfile`: Python dependencies management

## Setup

1. Ensure you have Python 3.10 installed.
2. Install pipenv: `pip install pipenv`
3. Install dependencies: `pipenv install`

## Running the Application

1. Make sure NordVPN CLI is installed and configured on your system.
2. Run the start script: `./start.sh`
3. you can change the port by setting the `NORDVPN_UI_PORT` environment variable.

The script will start the FastAPI backend, which also serves the static HTML file.

- API Swagger UI: http://localhost:8000/docs
- Web UI: http://localhost:8000/static/index.html

## Features

- View NordVPN connection status
- Connect to specific countries or groups
- Disconnect from VPN
- View and modify NordVPN settings
- Select VPN technology (NordLynx or OpenVPN)
- Choose VPN protocol (TCP or UDP)
- Run speed tests

## API Endpoints

- GET `/status`: Retrieve current VPN status
- GET `/countries`: Get list of available countries
- POST `/connect/{country}`: Connect to a specific country
- POST `/connect/group/{group}`: Connect to a specific group
- GET `/technologies`: List available VPN technologies
- GET `/protocols`: List available VPN protocols
- POST `/set/{setting}/{value}`: Modify a NordVPN setting
- GET `/settings`: Retrieve current NordVPN settings
- POST `/disconnect`: Disconnect from VPN
- GET `/speedtest`: Run a speed test
- GET `/groups`: Get list of available groups

## Note

Ensure that you have the necessary permissions to run NordVPN commands on your system.
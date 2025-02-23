import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import subprocess
import speedtest  # Add this import
import logging
import dotenv

dotenv.load_dotenv()
# Get port from environment variable, default to 8000 if not set
PORT = int(os.getenv('NORDVPN_UI_PORT', 8000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


PRIORITY_COUNTRIES = ["United_Kingdom", "Belgium", "France", "Netherlands"]

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")

@app.get("/status")
async def get_status():
    status_output = run_command(["nordvpn", "status"])
    status_lines = status_output.split('\n')
    status_dict = {}
    for line in status_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            status_dict[key.strip()] = value.strip()
    return status_dict

@app.get("/countries")
async def get_countries():
    countries = run_command(["nordvpn", "countries"])
    all_countries = [country.strip() for country in countries.split() if country.strip()]
    priority_countries = [country for country in PRIORITY_COUNTRIES if country in all_countries]
    other_countries = [country for country in all_countries if country not in PRIORITY_COUNTRIES]
    return {"priority": priority_countries, "other": other_countries}

@app.post("/connect/{country}")
async def connect_country(country: str):
    return run_command(["nordvpn", "connect", country])

@app.get("/technologies")
async def get_technologies():
    return ["NORDLYNX", "OPENVPN"]

@app.get("/protocols")
async def get_protocols():
    return ["TCP", "UDP"]

@app.post("/set/{setting}/{value}")
async def set_setting(setting: str, value: str):
    return run_command(["nordvpn", "set", setting, value])

@app.get("/settings")
async def get_settings():
    settings_output = run_command(["nordvpn", "settings"])
    settings_lines = settings_output.split('\n')
    settings_dict = {}
    current_key = None
    for line in settings_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            if value:
                settings_dict[key] = value
            else:
                current_key = key
                settings_dict[current_key] = []
        elif current_key and line.strip():
            settings_dict[current_key].append(line.strip())
    return settings_dict

@app.post("/disconnect")
async def disconnect():
    return run_command(["nordvpn", "disconnect"])

@app.get("/speedtest")
async def run_speedtest():
    try:
        logger.info("Starting speedtest")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping
        result = {
            "download": round(download_speed, 2),
            "upload": round(upload_speed, 2),
            "ping": round(ping, 2)
        }
        logger.info(f"Speedtest completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Speedtest failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speedtest failed: {str(e)}")

@app.get("/groups")
async def get_groups():
    groups = run_command(["nordvpn", "groups"])
    return [group.strip() for group in groups.split() if group.strip()]

@app.post("/connect/group/{group}")
async def connect_group(group: str):
    return run_command(["nordvpn", "connect", group])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=PORT, reload=True)

from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

PRIORITY_COUNTRIES = ["United_Kingdom", "Belgium", "France", "Netherlands"]

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Command failed: {e.stderr}")

@app.get("/status")
async def get_status():
    status = run_command(["nordvpn", "status"])
    return status

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
    return run_command(["nordvpn", "settings"])

@app.post("/disconnect")
async def disconnect():
    return run_command(["nordvpn", "disconnect"])

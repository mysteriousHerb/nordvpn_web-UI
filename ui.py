import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

st.title("NordVPN Control Panel")

COUNTRY_FLAGS = {
    "United_Kingdom": "🇬🇧",
    "Belgium": "🇧🇪",
    "France": "🇫🇷",
    "Netherlands": "🇳🇱"
}

def get_status():
    response = requests.get(f"{API_URL}/status")
    return response.text

def get_countries():
    response = requests.get(f"{API_URL}/countries")
    return response.json()

def get_technologies():
    response = requests.get(f"{API_URL}/technologies")
    return response.json()

def get_protocols():
    response = requests.get(f"{API_URL}/protocols")
    return response.json()

def get_settings():
    response = requests.get(f"{API_URL}/settings")
    return response.text

def set_setting(setting, value):
    response = requests.post(f"{API_URL}/set/{setting}/{value}")
    return response.text

def clean_status_line(line):
    return line.split(": ", 1)[-1] if ": " in line else line

def refresh_status():
    status = get_status()
    
    # Remove surrounding quotes and split by actual newlines
    status = status.strip('"').replace("\\n", "\n")
    status_lines = status.split('\n')
    
    connection_status = next((clean_status_line(line) for line in status_lines if line.startswith("Status:")), "Unknown")
    current_server = next((clean_status_line(line) for line in status_lines if line.startswith("Server:")), "Unknown")
    return status, connection_status, current_server

# Response display area
response_area = st.empty()

# Highlight key status information
status_placeholder = st.empty()
server_placeholder = st.empty()

def update_status_display():
    status, connection_status, current_server = refresh_status()
    status_placeholder.write(f"**Status: {connection_status if connection_status != 'Unknown' else 'Not available'}**")
    server_placeholder.write(f"**Server: {current_server if current_server != 'Unknown' else 'Not available'}**")
    return status

status = update_status_display()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Connect to Country")
    countries = get_countries()
    
    st.write("Priority Countries:")
    priority_cols = st.columns(len(countries["priority"]))
    for i, country in enumerate(countries["priority"]):
        if priority_cols[i].button(COUNTRY_FLAGS.get(country, country)):
            st.session_state.selected_country = country

    st.write("All Countries:")
    all_countries = [""] + countries["priority"] + countries["other"]
    selected_country = st.selectbox("Select a country", all_countries, key="selected_country", index=all_countries.index("United_Kingdom"))

with col2:
    st.subheader("Change Settings")
    setting_options = [
        "technology", "protocol", "killswitch", "autoconnect", "dns", "lan"
    ]

    selected_setting = st.selectbox("Select setting to change", setting_options)

    if selected_setting == "technology":
        technologies = get_technologies()
        value = st.selectbox(f"Select {selected_setting}", technologies)
    elif selected_setting == "protocol":
        protocols = get_protocols()
        value = st.selectbox(f"Select {selected_setting}", protocols)
    elif selected_setting in ["killswitch", "autoconnect", "lan"]:
        value = st.selectbox(f"Set {selected_setting}", ["enabled", "disabled"])
    elif selected_setting == "dns":
        value = st.text_input("Enter DNS server (e.g., 1.1.1.1)")
    
    if st.button(f"Apply {selected_setting.capitalize()}"):
        response = set_setting(selected_setting, value)
        response_area.success(f"Setting {selected_setting} updated")
        response_area.code(response.replace("\\n", "\n"))

# Buttons for Connect, Disconnect, and Refresh
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Connect") and selected_country:
        response = requests.post(f"{API_URL}/connect/{selected_country}")
        response_area.success(f"Connected to {selected_country}")
        response_area.code(response.text.replace("\\n", "\n"))
        status = update_status_display()
with col2:
    if st.button("Disconnect"):
        response = requests.post(f"{API_URL}/disconnect")
        response_area.success("Disconnected from NordVPN")
        response_area.code(response.text.replace("\\n", "\n"))
        status = update_status_display()
with col3:
    if st.button("Refresh Status"):
        status = update_status_display()

# Detailed Status and Settings at the bottom
st.subheader("Detailed Information")
info_type = st.selectbox("Select information to display", ["Status", "Settings"])

if info_type == "Status":
    st.text("Current Status:")
    st.code(status.replace("\\n", "\n").replace('"', ''))
else:
    settings = get_settings()
    st.text("Current Settings:")
    st.code(settings.replace("\\n", "\n").replace('"', ''))

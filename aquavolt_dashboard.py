import streamlit as st
import requests
from datetime import datetime

# === CONFIG ===
BLYNK_TOKEN = "IORkfzg0h_mdfX_srvneGMPBOyT4DpPz"
BASE_URL = "https://blynk.cloud/external/api"

# === FUNCTIONS ===
def get_blynk_value(pin):
    """Fetch latest value from a Blynk virtual pin"""
    url = f"{BASE_URL}/get?token={BLYNK_TOKEN}&{pin}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return float(r.text)
        else:
            return None
    except Exception as e:
        st.error(f"Blynk fetch error: {e}")
        return None

def send_blynk_value(pin, value):
    """Send control value to Blynk virtual pin"""
    url = f"{BASE_URL}/update?token={BLYNK_TOKEN}&{pin}={value}"
    try:
        requests.get(url)
    except Exception as e:
        st.error(f"Error sending command: {e}")

def get_blynk_alerts():
    """Fetch latest log events (alerts)"""
    url = f"{BASE_URL}/logs?token={BLYNK_TOKEN}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            return []
    except Exception as e:
        st.error(f"Blynk log error: {e}")
        return []

# === PAGE ===
st.set_page_config(page_title="AquaVolt IoT Dashboard", page_icon="💧", layout="wide")
st.title("🌊 AquaVolt IoT Dashboard")

# === LIVE DATA ===
col1, col2 = st.columns(2)
with col1:
    water = get_blynk_value("V1")   # totalMilliLitres
    if water is not None:
        st.metric("💧 Water Used", f"{water:.2f} L")
    else:
        st.warning("No water data yet")

with col2:
    current = get_blynk_value("V0")  # current RMS
    if current is not None:
        st.metric("⚡ Current (RMS)", f"{current:.2f} mA")
    else:
        st.warning("No current data yet")

st.divider()

# === CONTROL SECTION ===
st.subheader("🧠 Device Control")
col3, col4 = st.columns(2)
with col3:
    if st.button("▶️ Forward ON"):
        send_blynk_value("V2", 0)
    if st.button("⏹ Forward OFF"):
        send_blynk_value("V2", 1)
with col4:
    if st.button("🔄 Backward ON"):
        send_blynk_value("V3", 0)
    if st.button("⏹ Backward OFF"):
        send_blynk_value("V3", 1)

st.divider()

# === ALERTS SECTION ===
st.subheader("🚨 Active Alerts")
alerts = get_blynk_alerts()
if alerts:
    for alert in alerts:
        st.warning(f"⚠️ {alert['type'].upper()} — {alert['body']}")
else:
    st.info("✅ No active alerts right now")

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data via Blynk Cloud")

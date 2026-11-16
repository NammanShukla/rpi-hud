from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

THEMES_DIR = BASE_DIR / "themes"
CONFIG_DIR = BASE_DIR / "config"

SERVER_URL = "http://192.168.0.100:5000/stats"

CITY_NAME = "New Delhi"

# New Delhi city centre coordinates
LATITUDE = 28.6139
LONGITUDE = 77.2090

TIMEZONE = "Asia/Kolkata"

# Refresh intervals (milliseconds)
SERVER_REFRESH = 5000
WEATHER_REFRESH = 900000       # 15 minutes
AQI_REFRESH = 600000           # 10 minutes
SYSTEM_REFRESH = 5000

THEME_CHECK_INTERVAL = 30000   # 30 seconds
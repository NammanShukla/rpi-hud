import tkinter as tk
import os

from dotenv import load_dotenv

from core.theme_manager import ThemeManager

from services.weather_service import WeatherService
from services.air_quality_service import AirQualityService
from services.server_service import ServerService
from services.system_service import SystemService

from widgets.dashboard import Dashboard


def main():

    load_dotenv()

    api_key = os.getenv("OPEN_WEATHER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENWEATHER_API_KEY missing from .env"
        )

    root = tk.Tk()

    # Initialize services
    server_service = ServerService()
    weather_service = WeatherService(api_key)
    air_service = AirQualityService(api_key)
    system_service = SystemService()

    # Initialize dashboard
    dashboard = Dashboard(
        root,
        server_service,
        weather_service,
        air_service,
        system_service
    )

    # Initialize independent theme engine
    theme_manager = ThemeManager(
        dashboard.apply_theme
    )

    # Detect and apply current theme immediately
    theme_manager.start(root)

    # Start dashboard updates after the GUI enters its event loop
    root.after(0, dashboard.start)

    root.mainloop()


if __name__ == "__main__":
    main()
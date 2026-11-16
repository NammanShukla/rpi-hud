import requests

from config.settings import (
    LATITUDE,
    LONGITUDE
)


# CPCB concentration breakpoints and AQI breakpoints
BREAKPOINTS = {
    "pm2_5": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, float("inf"), 401, 500)
    ],

    "pm10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, float("inf"), 401, 500)
    ]
}


def calculate_subindex(pollutant, concentration):

    if concentration is None or concentration < 0:
        return None

    ranges = BREAKPOINTS[pollutant]

    for blo, bhi, ilo, ihi in ranges:

        if blo <= concentration <= bhi:

            if bhi == float("inf"):
                return 500

            index = (
                (ihi - ilo) / (bhi - blo)
            ) * (concentration - blo) + ilo

            return round(index)

    return None


class AirQualityService:

    def __init__(self, api_key):

        self.api_key = api_key

    def fetch(self):

        try:

            url = "https://api.openweathermap.org/data/2.5/air_pollution"

            params = {
                "lat": LATITUDE,
                "lon": LONGITUDE,
                "appid": self.api_key
            }

            response = requests.get(
                url,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            reading = data["list"][0]

            components = reading["components"]

            pm25 = components["pm2_5"]
            pm10 = components["pm10"]

            owm_aqi = reading["main"]["aqi"]

            return {
                "owm_aqi": owm_aqi,

                "aqi_label": {
                    1: "Good",
                    2: "Fair",
                    3: "Moderate",
                    4: "Poor",
                    5: "Very Poor"
                }.get(owm_aqi, "Unknown"),

                "pm25": round(pm25, 1),
                "pm10": round(pm10, 1),

                "pm25_subindex": calculate_subindex(
                    "pm2_5", pm25
                ),

                "pm10_subindex": calculate_subindex(
                    "pm10", pm10
                ),

                "timestamp": reading["dt"]
            }

        except requests.RequestException as error:

            print(f"AQI error: {error}")

        except (KeyError, IndexError, TypeError) as error:

            print(f"Invalid AQI response: {error}")

        return None
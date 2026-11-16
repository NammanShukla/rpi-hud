import requests

from config.settings import (
    CITY_NAME
)


class WeatherService:

    def __init__(self, api_key):

        self.api_key = api_key

    def fetch(self):

        try:

            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": CITY_NAME,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(
                url,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title()
            }

        except requests.RequestException as error:

            print(f"Weather error: {error}")

        except (KeyError, IndexError, TypeError) as error:

            print(f"Invalid weather response: {error}")

        return None
import requests

from config.settings import SERVER_URL


class ServerService:

    def fetch(self):

        try:

            response = requests.get(
                SERVER_URL,
                timeout=3
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:

            print(f"Server connection error: {error}")

        return None
import requests


def fetch_weather(latitude, longitude):

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "precipitation,"
                    "wind_speed_10m"
                ),
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as exc:
        return {
            "error": str(exc)
        }

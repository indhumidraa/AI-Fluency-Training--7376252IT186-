import requests


def get_current_weather(city):
    # Geocoding: convert city name to latitude/longitude
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=10,
    )

    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if "results" not in geo_data or not geo_data["results"]:
        return f"Could not find the location: {city}"

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    )

    weather_response.raise_for_status()
    weather_data = weather_response.json()

    current = weather_data["current"]

    return (
        f"Current weather in {city}: "
        f"{current['temperature_2m']}°C, "
        f"humidity {current['relative_humidity_2m']}%."
    )


if __name__ == "__main__":
    print(get_current_weather("Chennai"))
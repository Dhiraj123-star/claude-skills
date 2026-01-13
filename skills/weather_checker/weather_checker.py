import requests

def weather_checker(location):
    """
    Takes a city name and returns the current temperature and weather description.
    No API Key required.
    """
    try:
        # 1. Geocoding: Get coordinates for the city name
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&format=json"
        geo_res = requests.get(geo_url)
        geo_data = geo_res.json()

        if not geo_data.get("results"):
            return {"error": f"City '{location}' not found."}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # 2. Weather: Get temperature using coordinates
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url)
        weather_data = weather_res.json()

        if "current_weather" not in weather_data:
            return {"error": "Weather data unavailable."}

        current = weather_data["current_weather"]
        
        # Mapping WMO codes to readable text
        weather_desc = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
            61: "Slight rain", 71: "Slight snow", 95: "Thunderstorm"
        }
        
        condition = weather_desc.get(current['weathercode'], "Unknown")

        # Return a clean dictionary for Claude to read
        return {
            "city": location.capitalize(),
            "temperature": f"{current['temperature']}°C",
            "condition": condition
        }

    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}


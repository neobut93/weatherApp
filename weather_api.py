import requests
import json
from datetime import datetime, timedelta
from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = OPENWEATHER_BASE_URL
    
    def get_current_weather(self, city, country_code="", units="metric"):
        """Get current weather data for a city"""
        try:
            location = f"{city},{country_code}" if country_code else city
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_forecast(self, city, country_code="", units="metric"):
        """Get 5-day weather forecast for a city"""
        try:
            location = f"{city},{country_code}" if country_code else city
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_weather_by_coordinates(self, lat, lon, units="metric"):
        """Get weather data by coordinates"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

def format_weather_data(weather_data):
    """Format weather data for display"""
    if "error" in weather_data:
        return weather_data
    
    try:
        formatted = {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temperature": round(weather_data["main"]["temp"]),
            "feels_like": round(weather_data["main"]["feels_like"]),
            "description": weather_data["weather"][0]["description"].title(),
            "icon": weather_data["weather"][0]["icon"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "wind_speed": weather_data["wind"]["speed"],
            "wind_direction": weather_data["wind"].get("deg", 0),
            "visibility": weather_data.get("visibility", 0) / 1000,  # Convert to km
            "uv_index": weather_data.get("uvi", 0),
            "timestamp": datetime.fromtimestamp(weather_data["dt"])
        }
        return formatted
    except KeyError as e:
        return {"error": f"Data formatting error: Missing key {str(e)}"}

def format_forecast_data(forecast_data):
    """Format forecast data for display"""
    if "error" in forecast_data:
        return forecast_data
    
    try:
        formatted_forecast = []
        for item in forecast_data["list"]:
            formatted_item = {
                "datetime": datetime.fromtimestamp(item["dt"]),
                "temperature": round(item["main"]["temp"]),
                "feels_like": round(item["main"]["feels_like"]),
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "wind_speed": item["wind"]["speed"],
                "precipitation": item.get("rain", {}).get("3h", 0) + item.get("snow", {}).get("3h", 0)
            }
            formatted_forecast.append(formatted_item)
        
        return {
            "city": forecast_data["city"]["name"],
            "country": forecast_data["city"]["country"],
            "forecast": formatted_forecast
        }
    except KeyError as e:
        return {"error": f"Forecast formatting error: Missing key {str(e)}"}


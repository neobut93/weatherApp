import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"

# App Configuration
APP_TITLE = "🌤️ Weather App"
DEFAULT_CITY = "London"
DEFAULT_COUNTRY = "UK"

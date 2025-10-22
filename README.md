# 🌤️ Weather App

A beautiful and feature-rich weather application built with Python and Streamlit. Get current weather conditions, 5-day forecasts, interactive maps, and weather alerts for any city worldwide.

## ✨ Features

### 🌡️ Current Weather
- Real-time weather conditions
- Temperature, humidity, wind speed, pressure
- Weather descriptions and icons
- Feels-like temperature
- Visibility and UV index

### 📈 5-Day Forecast
- Interactive temperature charts
- Humidity and wind speed trends
- Detailed forecast table
- Visual temperature ranges

### 🗺️ Interactive Weather Map
- Location-based weather visualization
- Custom weather markers
- Clickable weather information

### 🚨 Weather Alerts & Recommendations
- Extreme temperature warnings
- High wind alerts
- Low visibility warnings
- UV index alerts
- Weather-based recommendations

### 📊 Advanced Visualizations
- Temperature range charts
- Humidity trends
- Wind speed graphs
- Weather summary cards

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenWeather API key (free at [openweathermap.org](https://openweathermap.org/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd WeatherApp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   Create a `.env` file in the project root:
   ```bash
   echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
   ```
   
   Or set as environment variable:
   ```bash
   export OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables
- `OPENWEATHER_API_KEY`: Your OpenWeather API key (required)

### App Settings
Edit `config.py` to customize:
- Default city and country
- API endpoints
- App title and branding

## 📱 Usage

1. **Search for a city**: Enter city name and country code in the sidebar
2. **Choose units**: Select metric (°C) or imperial (°F) units
3. **View current weather**: See real-time conditions and metrics
4. **Check forecasts**: Browse 5-day temperature and weather trends
5. **Explore the map**: View weather on an interactive map
6. **Review alerts**: Check for weather warnings and recommendations

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with requests for API calls
- **Data Processing**: Pandas for data manipulation
- **Visualizations**: Plotly for interactive charts
- **Maps**: Folium for interactive mapping

### API Integration
- **OpenWeather API**: Current weather and 5-day forecast
- **Error Handling**: Comprehensive error management
- **Rate Limiting**: Built-in API call optimization

### File Structure
```
WeatherApp/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── weather_api.py        # API integration and data formatting
├── weather_visualizations.py  # Chart and map creation
├── weather_alerts.py     # Alert system and recommendations
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎨 Customization

### Styling
Modify the CSS in `app.py` to customize:
- Color schemes
- Card designs
- Typography
- Layout spacing

### Features
Add new features by:
- Extending `weather_api.py` for new data sources
- Adding visualizations in `weather_visualizations.py`
- Creating new alert types in `weather_alerts.py`

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenWeather API key is valid
   - Check that the key is properly set in `.env` file

2. **City Not Found**
   - Try different city names
   - Include country code for better accuracy
   - Check spelling and formatting

3. **Map Not Loading**
   - Ensure internet connection
   - Check if coordinates are valid
   - Try refreshing the page

### Performance
- The app caches API responses for better performance
- Large datasets are optimized for smooth rendering
- Charts use Plotly's efficient rendering engine

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, please open an issue in the repository or contact the development team.

---

**Enjoy your weather app! 🌤️**

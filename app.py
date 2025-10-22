import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from streamlit_folium import st_folium

# Import our custom modules
from config import APP_TITLE, DEFAULT_CITY, DEFAULT_COUNTRY, OPENWEATHER_API_KEY
from weather_api import WeatherAPI, format_weather_data, format_forecast_data
from weather_visualizations import (
    create_temperature_chart, 
    create_humidity_chart, 
    create_wind_chart,
    create_weather_map,
    create_weather_summary_cards,
    create_hourly_forecast_chart,
    create_daily_forecast_cards
)
from weather_alerts import WeatherAlerts
from countries_cities import get_countries, get_country_code, get_cities
from states_cities import get_states, get_cities_by_state, get_country_code_from_states

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .alert-container {
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .recommendation-item {
        background: rgba(46, 125, 50, 0.1);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #2e7d32;
    }
    
    .search-section {
        margin-bottom: 1.5rem;
    }
    
    .input-row {
        display: flex;
        gap: 1rem;
        align-items: end;
        margin-bottom: 1rem;
    }
    
    .input-group {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    
    .input-group label {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #262730;
    }
    
    .input-group input {
        width: 100%;
    }
    
    .search-mode {
        margin-bottom: 1rem;
    }
    
    .search-mode .stRadio > div {
        gap: 0.5rem;
    }
    
    .search-mode .stRadio > div > label {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        background: white;
        transition: all 0.3s ease;
    }
    
    .search-mode .stRadio > div > label:hover {
        border-color: #4CAF50;
        background: #f8f9fa;
    }
    
    .search-mode .stRadio > div > label[data-testid="stRadio"] {
        margin-right: 0.5rem;
    }
    
    .manual-format {
        background: #f0f8ff;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 0.5rem 0;
    }
    
    .daily-forecast-container {
        display: flex;
        gap: 0.5rem;
        overflow-x: auto;
        padding: 0.5rem 0;
    }
    
    .daily-card {
        min-width: 120px;
        flex-shrink: 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }
    
    /* Daily forecast cards */
    .daily-forecast-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.25rem;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown(f'<h1 class="main-header">{APP_TITLE}</h1>', unsafe_allow_html=True)
    
    # Initialize weather API and alerts
    if OPENWEATHER_API_KEY == 'your_api_key_here':
        st.error("⚠️ Please set your OpenWeather API key in the .env file or environment variables!")
        st.info("Get your free API key from https://openweathermap.org/api")
        return
    
    weather_api = WeatherAPI(OPENWEATHER_API_KEY)
    alerts_system = WeatherAlerts()
    
    # Sidebar for user input
    with st.sidebar:
        st.markdown("### 🔍 Search Location")
        
        # Search mode toggle
        st.markdown('<div class="search-mode">', unsafe_allow_html=True)
        search_mode = st.radio(
            "Search Mode",
            ["🌍 Country & City", "🏛️ State & City", "✍️ Manual Entry"],
            help="Choose how you want to search for your location"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if search_mode == "🌍 Country & City":
            # Country selection
            countries = get_countries()
            selected_country = st.selectbox(
                "Select Country", 
                options=countries,
                index=countries.index("United Kingdom") if "United Kingdom" in countries else 0,
                help="Choose your country from the list"
            )
            
            # City selection based on country
            cities = get_cities(selected_country)
            
            # Add option to search manually
            search_manually = st.checkbox("Search manually", help="Check this if your city is not in the list")
            
            if not search_manually and cities:
                # Find default city in the list or use first city
                default_city_index = 0
                if DEFAULT_CITY in cities:
                    default_city_index = cities.index(DEFAULT_CITY)
                elif "London" in cities:
                    default_city_index = cities.index("London")
                
                selected_city = st.selectbox(
                    "Select City",
                    options=cities,
                    index=default_city_index,
                    help="Choose your city from the list"
                )
            else:
                selected_city = st.text_input("Enter City Name", value=DEFAULT_CITY, help="Enter the name of your city")
            
            # Get country code for API
            country_code = get_country_code(selected_country)
            city = selected_city
            country = country_code
            
        elif search_mode == "🏛️ State & City":
            # Country selection for states
            countries_with_states = ["United States", "Canada", "Australia"]
            selected_country = st.selectbox(
                "Select Country", 
                options=countries_with_states,
                index=0,
                help="Choose a country with state/province data"
            )
            
            # State selection
            states = get_states(selected_country)
            if states:
                selected_state = st.selectbox(
                    "Select State/Province",
                    options=states,
                    help="Choose your state or province"
                )
                
                # City selection based on state
                cities = get_cities_by_state(selected_country, selected_state)
                if cities:
                    selected_city = st.selectbox(
                        "Select City",
                        options=cities,
                        help="Choose your city from the list"
                    )
                else:
                    selected_city = st.text_input("Enter City Name", value="", help="Enter the name of your city")
            else:
                selected_city = st.text_input("Enter City Name", value="", help="Enter the name of your city")
            
            # Get country code for API
            country_code = get_country_code_from_states(selected_country)
            city = selected_city
            country = country_code
            
        else:  # Manual Entry
            st.markdown("""
            <div class="manual-format">
                <strong>Format:</strong> <code>City, Country Code</code><br>
                <em>Examples:</em> <code>Tracy, CA</code> or <code>London, GB</code>
            </div>
            """, unsafe_allow_html=True)
            
            manual_input = st.text_input(
                "Enter Location", 
                value="London, GB", 
                help="Enter city and country code separated by comma"
            )
            
            if manual_input and "," in manual_input:
                parts = manual_input.split(",", 1)
                city = parts[0].strip()
                country = parts[1].strip()
            else:
                city = manual_input
                country = ""
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Units selection
        units = st.selectbox("Temperature Units", ["metric", "imperial"], index=0)
        unit_symbol = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"
        
        # Add some spacing
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Additional options
        st.markdown("---")
        st.markdown("### 📊 Display Options")
        show_map = st.checkbox("Show Weather Map", value=True)
        show_alerts = st.checkbox("Show Weather Alerts", value=True)
        show_recommendations = st.checkbox("Show Recommendations", value=True)
    
    # Main content area
    if city:
        # Get weather data
        with st.spinner("Fetching weather data..."):
            current_weather = weather_api.get_current_weather(city, country, units)
            forecast_data = weather_api.get_forecast(city, country, units)
        
        # Check for API errors
        if "error" in current_weather:
            st.error(f"❌ Error: {current_weather['error']}")
            return
        
        if "error" in forecast_data:
            st.error(f"❌ Error: {forecast_data['error']}")
            return
        
        # Format data
        formatted_current = format_weather_data(current_weather)
        formatted_forecast = format_forecast_data(forecast_data)
        
        # Current Weather Section - Combined Card
        st.markdown("## 🌤️ Current Weather")
        
        # Weather icon mapping
        weather_icons = {
            "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️",
            "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️"
        }
        icon = weather_icons.get(formatted_current['icon'], "🌤️")
        
        # Create compact weather display using only Streamlit components
        st.markdown("---")
        
        # Three columns for the layout
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            # Left: Weather Icon and Temperature
            st.markdown(f"# {icon}")
            st.markdown(f"# {formatted_current['temperature']}{unit_symbol}")
        
        with col2:
            # Middle: Weather Details
            st.markdown("**Weather Details**")
            st.markdown(f"Precipitation: {formatted_current.get('precipitation', 0)}%")
            st.markdown(f"Humidity: {formatted_current.get('humidity', 0)}%")
            st.markdown(f"Wind: {formatted_current.get('wind_speed', 0)} m/s")
        
        with col3:
            # Right: Weather Info
            st.markdown("**Weather**")
            st.markdown(f"{formatted_current['timestamp'].strftime('%A %I:%M %p')}")
            st.markdown(f"{formatted_current['description']}")
        
        st.markdown("---")
        
        # Weather Forecast with Tabs
        st.markdown("## 📈 Detailed Forecast")
        
        # Create tabs for different metrics
        tab1, tab2, tab3 = st.tabs(["🌡️ Temperature", "🌧️ Precipitation", "💨 Wind"])
        
        with tab1:
            # Hourly temperature chart
            temp_chart = create_hourly_forecast_chart(formatted_forecast, "temperature")
            if temp_chart:
                st.plotly_chart(temp_chart, use_container_width=True)
        
        with tab2:
            # Hourly precipitation chart
            precip_chart = create_hourly_forecast_chart(formatted_forecast, "precipitation")
            if precip_chart:
                st.plotly_chart(precip_chart, use_container_width=True)
        
        with tab3:
            # Hourly wind chart
            wind_chart = create_hourly_forecast_chart(formatted_forecast, "wind")
            if wind_chart:
                st.plotly_chart(wind_chart, use_container_width=True)
        
        # Daily forecast cards
        st.markdown("### 📅 7-Day Forecast")
        daily_cards = create_daily_forecast_cards(formatted_forecast)
        
        if daily_cards:
            # Create a horizontal scrollable container for daily cards
            cols = st.columns(7)
            for i, card in enumerate(daily_cards):
                with cols[i]:
                    st.markdown(f"""
                    <div class="daily-forecast-card">
                        <div style="font-weight: 600; margin-bottom: 0.5rem; color: #333;">
                            {card['day']}
                        </div>
                        <div style="font-size: 1.5rem; margin: 0.5rem 0;">
                            {card['icon']}
                        </div>
                        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">
                            {card['description']}
                        </div>
                        <div style="font-weight: 600; color: #333;">
                            {card['max_temp']}° {card['min_temp']}°
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Weather Alerts
        if show_alerts:
            st.markdown("## 🚨 Weather Alerts & Recommendations")
            
            alerts = alerts_system.check_weather_alerts(formatted_current)
            alerts_system.display_alerts(alerts)
            
            if show_recommendations:
                recommendations = alerts_system.get_weather_recommendations(formatted_current)
                if recommendations:
                    st.markdown("### 💡 Weather Recommendations")
                    for rec in recommendations:
                        st.markdown(f"""
                        <div class="recommendation-item">
                            {rec}
                        </div>
                        """, unsafe_allow_html=True)
        
        # Weather Map
        if show_map:
            st.markdown("## 🗺️ Weather Map")
            try:
                lat = current_weather['coord']['lat']
                lon = current_weather['coord']['lon']
                weather_map = create_weather_map(lat, lon, formatted_current['city'], formatted_current)
                if weather_map:
                    st_folium(weather_map, width=700, height=500)
            except Exception as e:
                st.warning(f"Could not load map: {str(e)}")
        
        # Forecast Section
        st.markdown("## 📈 5-Day Forecast")
        
        # Temperature Chart
        temp_chart = create_temperature_chart(formatted_forecast)
        if temp_chart:
            st.plotly_chart(temp_chart, use_container_width=True)
        
        # Additional Charts
        col1, col2 = st.columns(2)
        
        with col1:
            humidity_chart = create_humidity_chart(formatted_forecast)
            if humidity_chart:
                st.plotly_chart(humidity_chart, use_container_width=True)
        
        with col2:
            wind_chart = create_wind_chart(formatted_forecast)
            if wind_chart:
                st.plotly_chart(wind_chart, use_container_width=True)
        
        # Detailed Forecast Table
        st.markdown("### 📋 Detailed Forecast")
        if "forecast" in formatted_forecast:
            forecast_df = pd.DataFrame(formatted_forecast["forecast"])
            forecast_df['Date'] = forecast_df['datetime'].dt.strftime('%Y-%m-%d')
            forecast_df['Time'] = forecast_df['datetime'].dt.strftime('%H:%M')
            forecast_df['Temperature'] = forecast_df['temperature'].astype(str) + unit_symbol
            forecast_df['Wind Speed'] = forecast_df['wind_speed'].astype(str) + f" {speed_unit}"
            forecast_df['Humidity'] = forecast_df['humidity'].astype(str) + "%"
            forecast_df['Pressure'] = forecast_df['pressure'].astype(str) + " hPa"
            
            display_df = forecast_df[['Date', 'Time', 'Temperature', 'description', 'Humidity', 'Wind Speed', 'Pressure']]
            st.dataframe(display_df, use_container_width=True)
    
    else:
        # Welcome screen
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <h2>Welcome to the Weather App! 🌤️</h2>
            <p style="font-size: 1.2rem; color: #666;">
                Enter a city name in the sidebar to get started with current weather and 5-day forecast.
            </p>
            <div style="margin-top: 2rem;">
                <h3>Features:</h3>
                <ul style="text-align: left; display: inline-block;">
                    <li>🌡️ Current weather conditions</li>
                    <li>📈 5-day weather forecast</li>
                    <li>🗺️ Interactive weather map</li>
                    <li>🚨 Weather alerts and recommendations</li>
                    <li>📊 Detailed weather metrics</li>
                    <li>📱 Responsive design</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

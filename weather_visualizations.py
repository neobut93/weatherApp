import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

def create_temperature_chart(forecast_data):
    """Create temperature forecast chart"""
    if "error" in forecast_data:
        return None
    
    df = pd.DataFrame(forecast_data["forecast"])
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    
    # Group by date and get min/max temperatures
    daily_temps = df.groupby('date').agg({
        'temperature': ['min', 'max', 'mean'],
        'datetime': 'first'
    }).reset_index()
    
    daily_temps.columns = ['date', 'min_temp', 'max_temp', 'avg_temp', 'datetime']
    
    fig = go.Figure()
    
    # Add temperature range
    fig.add_trace(go.Scatter(
        x=daily_temps['date'],
        y=daily_temps['max_temp'],
        fill=None,
        mode='lines',
        line_color='rgba(255,0,0,0)',
        name='Max Temperature',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_temps['date'],
        y=daily_temps['min_temp'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,100,255,0)',
        name='Temperature Range',
        fillcolor='rgba(0,100,255,0.2)'
    ))
    
    # Add average temperature line
    fig.add_trace(go.Scatter(
        x=daily_temps['date'],
        y=daily_temps['avg_temp'],
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(size=8),
        name='Average Temperature'
    ))
    
    fig.update_layout(
        title="5-Day Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        template="plotly_white"
    )
    
    return fig

def create_humidity_chart(forecast_data):
    """Create humidity forecast chart"""
    if "error" in forecast_data:
        return None
    
    df = pd.DataFrame(forecast_data["forecast"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['datetime'],
        y=df['humidity'],
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=6),
        name='Humidity %'
    ))
    
    fig.update_layout(
        title="Humidity Forecast",
        xaxis_title="Date & Time",
        yaxis_title="Humidity (%)",
        hovermode='x unified',
        template="plotly_white"
    )
    
    return fig

def create_wind_chart(forecast_data):
    """Create wind speed chart"""
    if "error" in forecast_data:
        return None
    
    df = pd.DataFrame(forecast_data["forecast"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['datetime'],
        y=df['wind_speed'],
        mode='lines+markers',
        line=dict(color='green', width=2),
        marker=dict(size=6),
        name='Wind Speed (m/s)'
    ))
    
    fig.update_layout(
        title="Wind Speed Forecast",
        xaxis_title="Date & Time",
        yaxis_title="Wind Speed (m/s)",
        hovermode='x unified',
        template="plotly_white"
    )
    
    return fig

def create_weather_map(lat, lon, city_name, weather_data):
    """Create interactive weather map"""
    if "error" in weather_data:
        return None
    
    # Create map centered on the city
    m = folium.Map(
        location=[lat, lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add weather marker
    weather_icon = weather_data.get("icon", "01d")
    temp = weather_data.get("temperature", 0)
    description = weather_data.get("description", "Unknown")
    
    # Create custom icon
    icon_html = f"""
    <div style="
        background: linear-gradient(45deg, #87CEEB, #4682B4);
        border: 2px solid white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    ">
        {temp}°C
    </div>
    """
    
    # Add marker
    folium.Marker(
        [lat, lon],
        popup=f"""
        <div style="text-align: center;">
            <h3>{city_name}</h3>
            <p><strong>{temp}°C</strong></p>
            <p>{description}</p>
            <p>Humidity: {weather_data.get('humidity', 0)}%</p>
            <p>Wind: {weather_data.get('wind_speed', 0)} m/s</p>
        </div>
        """,
        icon=folium.DivIcon(
            html=icon_html,
            icon_size=(60, 60),
            icon_anchor=(30, 30)
        )
    ).add_to(m)
    
    return m

def create_weather_summary_cards(weather_data):
    """Create summary cards for weather metrics"""
    if "error" in weather_data:
        return None
    
    cards_data = [
        {
            "title": "Temperature",
            "value": f"{weather_data.get('temperature', 0)}°C",
            "subtitle": f"Feels like {weather_data.get('feels_like', 0)}°C",
            "icon": "🌡️"
        },
        {
            "title": "Humidity",
            "value": f"{weather_data.get('humidity', 0)}%",
            "subtitle": "Relative humidity",
            "icon": "💧"
        },
        {
            "title": "Wind Speed",
            "value": f"{weather_data.get('wind_speed', 0)} m/s",
            "subtitle": f"Direction: {weather_data.get('wind_direction', 0)}°",
            "icon": "💨"
        },
        {
            "title": "Pressure",
            "value": f"{weather_data.get('pressure', 0)} hPa",
            "subtitle": "Atmospheric pressure",
            "icon": "📊"
        },
        {
            "title": "Visibility",
            "value": f"{weather_data.get('visibility', 0):.1f} km",
            "subtitle": "Visibility range",
            "icon": "👁️"
        },
        {
            "title": "UV Index",
            "value": f"{weather_data.get('uv_index', 0)}",
            "subtitle": "UV radiation level",
            "icon": "☀️"
        }
    ]
    
    return cards_data

def create_hourly_forecast_chart(forecast_data, chart_type="temperature"):
    """Create hourly forecast chart for different metrics"""
    if "error" in forecast_data or "forecast" not in forecast_data:
        return None
    
    df = pd.DataFrame(forecast_data["forecast"])
    
    # Get next 24 hours of data
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day
    current_hour = datetime.now().hour
    
    # Filter to next 24 hours
    df_24h = df.head(8)  # 3-hour intervals for 24 hours
    
    if chart_type == "temperature":
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(go.Scatter(
            x=df_24h['datetime'],
            y=df_24h['temperature'],
            mode='lines+markers',
            line=dict(color='#FFA500', width=3),
            marker=dict(size=8, color='#FFA500'),
            name='Temperature',
            fill='tonexty',
            fillcolor='rgba(255, 165, 0, 0.2)'
        ))
        
        fig.update_layout(
            title="Hourly Temperature Forecast",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        # Format x-axis to show time
        fig.update_xaxes(
            tickformat="%I %p",
            tickmode='auto',
            nticks=8
        )
        
    elif chart_type == "precipitation":
        fig = go.Figure()
        
        # Add precipitation bars
        fig.add_trace(go.Bar(
            x=df_24h['datetime'],
            y=df_24h['precipitation'],
            marker_color='#4A90E2',
            name='Precipitation'
        ))
        
        fig.update_layout(
            title="Hourly Precipitation Forecast",
            xaxis_title="Time",
            yaxis_title="Precipitation (mm)",
            template="plotly_white",
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_xaxes(
            tickformat="%I %p",
            tickmode='auto',
            nticks=8
        )
        
    elif chart_type == "wind":
        fig = go.Figure()
        
        # Add wind speed line
        fig.add_trace(go.Scatter(
            x=df_24h['datetime'],
            y=df_24h['wind_speed'],
            mode='lines+markers',
            line=dict(color='#2ECC71', width=3),
            marker=dict(size=8, color='#2ECC71'),
            name='Wind Speed',
            fill='tonexty',
            fillcolor='rgba(46, 204, 113, 0.2)'
        ))
        
        fig.update_layout(
            title="Hourly Wind Speed Forecast",
            xaxis_title="Time",
            yaxis_title="Wind Speed (m/s)",
            template="plotly_white",
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_xaxes(
            tickformat="%I %p",
            tickmode='auto',
            nticks=8
        )
    
    return fig

def create_daily_forecast_cards(forecast_data):
    """Create daily forecast cards similar to the image"""
    if "error" in forecast_data or "forecast" not in forecast_data:
        return None
    
    df = pd.DataFrame(forecast_data["forecast"])
    
    # Group by date and get daily min/max
    df['date'] = df['datetime'].dt.date
    daily_data = df.groupby('date').agg({
        'temperature': ['min', 'max'],
        'description': 'first',
        'icon': 'first',
        'datetime': 'first'
    }).reset_index()
    
    daily_data.columns = ['date', 'min_temp', 'max_temp', 'description', 'icon', 'datetime']
    
    # Get next 7 days
    daily_data = daily_data.head(7)
    
    # Weather icons mapping
    weather_icons = {
        "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    
    cards = []
    for _, row in daily_data.iterrows():
        day_name = row['datetime'].strftime('%a')
        icon = weather_icons.get(row['icon'], "🌤️")
        description = row['description']
        max_temp = int(row['max_temp'])
        min_temp = int(row['min_temp'])
        
        cards.append({
            'day': day_name,
            'icon': icon,
            'description': description,
            'max_temp': max_temp,
            'min_temp': min_temp
        })
    
    return cards


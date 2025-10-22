from datetime import datetime, timedelta
import streamlit as st

class WeatherAlerts:
    def __init__(self):
        self.alert_types = {
            "extreme_temperature": {
                "hot": {"threshold": 35, "message": "🌡️ Extreme Heat Warning", "color": "red"},
                "cold": {"threshold": -10, "message": "🧊 Extreme Cold Warning", "color": "blue"}
            },
            "high_wind": {
                "threshold": 15,
                "message": "💨 High Wind Warning",
                "color": "orange"
            },
            "low_visibility": {
                "threshold": 1,
                "message": "🌫️ Low Visibility Warning",
                "color": "yellow"
            },
            "high_humidity": {
                "threshold": 80,
                "message": "💧 High Humidity Alert",
                "color": "blue"
            },
            "uv_warning": {
                "high": {"threshold": 8, "message": "☀️ High UV Warning", "color": "red"},
                "moderate": {"threshold": 6, "message": "☀️ Moderate UV Alert", "color": "orange"}
            }
        }
    
    def check_weather_alerts(self, weather_data):
        """Check current weather conditions for alerts"""
        if "error" in weather_data:
            return []
        
        alerts = []
        
        # Temperature alerts
        temp = weather_data.get("temperature", 0)
        if temp >= self.alert_types["extreme_temperature"]["hot"]["threshold"]:
            alerts.append({
                "type": "extreme_temperature",
                "severity": "high",
                "message": self.alert_types["extreme_temperature"]["hot"]["message"],
                "color": self.alert_types["extreme_temperature"]["hot"]["color"],
                "details": f"Temperature is {temp}°C - Stay hydrated and avoid prolonged sun exposure!"
            })
        elif temp <= self.alert_types["extreme_temperature"]["cold"]["threshold"]:
            alerts.append({
                "type": "extreme_temperature",
                "severity": "high",
                "message": self.alert_types["extreme_temperature"]["cold"]["message"],
                "color": self.alert_types["extreme_temperature"]["cold"]["color"],
                "details": f"Temperature is {temp}°C - Dress warmly and limit time outdoors!"
            })
        
        # Wind alerts
        wind_speed = weather_data.get("wind_speed", 0)
        if wind_speed >= self.alert_types["high_wind"]["threshold"]:
            alerts.append({
                "type": "high_wind",
                "severity": "medium",
                "message": self.alert_types["high_wind"]["message"],
                "color": self.alert_types["high_wind"]["color"],
                "details": f"Wind speed is {wind_speed} m/s - Be cautious when driving or walking!"
            })
        
        # Visibility alerts
        visibility = weather_data.get("visibility", 10)
        if visibility <= self.alert_types["low_visibility"]["threshold"]:
            alerts.append({
                "type": "low_visibility",
                "severity": "medium",
                "message": self.alert_types["low_visibility"]["message"],
                "color": self.alert_types["low_visibility"]["color"],
                "details": f"Visibility is only {visibility:.1f} km - Drive carefully!"
            })
        
        # Humidity alerts
        humidity = weather_data.get("humidity", 0)
        if humidity >= self.alert_types["high_humidity"]["threshold"]:
            alerts.append({
                "type": "high_humidity",
                "severity": "low",
                "message": self.alert_types["high_humidity"]["message"],
                "color": self.alert_types["high_humidity"]["color"],
                "details": f"Humidity is {humidity}% - High moisture levels detected!"
            })
        
        # UV alerts
        uv_index = weather_data.get("uv_index", 0)
        if uv_index >= self.alert_types["uv_warning"]["high"]["threshold"]:
            alerts.append({
                "type": "uv_warning",
                "severity": "high",
                "message": self.alert_types["uv_warning"]["high"]["message"],
                "color": self.alert_types["uv_warning"]["high"]["color"],
                "details": f"UV Index is {uv_index} - Use sunscreen and avoid sun exposure!"
            })
        elif uv_index >= self.alert_types["uv_warning"]["moderate"]["threshold"]:
            alerts.append({
                "type": "uv_warning",
                "severity": "medium",
                "message": self.alert_types["uv_warning"]["moderate"]["message"],
                "color": self.alert_types["uv_warning"]["moderate"]["color"],
                "details": f"UV Index is {uv_index} - Consider using sunscreen!"
            })
        
        return alerts
    
    def display_alerts(self, alerts):
        """Display weather alerts in the UI"""
        if not alerts:
            st.success("✅ No weather alerts at this time!")
            return
        
        # Sort alerts by severity
        severity_order = {"high": 0, "medium": 1, "low": 2}
        alerts.sort(key=lambda x: severity_order.get(x["severity"], 3))
        
        st.markdown("### 🚨 Weather Alerts")
        
        for alert in alerts:
            color_map = {
                "red": "🔴",
                "orange": "🟠", 
                "yellow": "🟡",
                "blue": "🔵"
            }
            
            icon = color_map.get(alert["color"], "⚪")
            
            with st.container():
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {alert['color']};
                    padding: 10px;
                    margin: 5px 0;
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 5px;
                ">
                    <h4 style="margin: 0; color: {alert['color']};">
                        {icon} {alert['message']}
                    </h4>
                    <p style="margin: 5px 0 0 0; font-size: 14px;">
                        {alert['details']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    def get_weather_recommendations(self, weather_data):
        """Get weather-based recommendations"""
        if "error" in weather_data:
            return []
        
        recommendations = []
        temp = weather_data.get("temperature", 0)
        description = weather_data.get("description", "").lower()
        wind_speed = weather_data.get("wind_speed", 0)
        humidity = weather_data.get("humidity", 0)
        uv_index = weather_data.get("uv_index", 0)
        
        # Temperature recommendations
        if temp > 25:
            recommendations.append("🌞 Perfect weather for outdoor activities!")
        elif temp > 15:
            recommendations.append("🌤️ Pleasant weather - great for a walk!")
        elif temp > 5:
            recommendations.append("🧥 Cool weather - consider a light jacket")
        else:
            recommendations.append("🧣 Cold weather - dress warmly!")
        
        # Weather condition recommendations
        if "rain" in description:
            recommendations.append("☔ Don't forget your umbrella!")
        elif "cloud" in description:
            recommendations.append("☁️ Overcast skies - good for photography!")
        elif "clear" in description or "sun" in description:
            recommendations.append("☀️ Clear skies - perfect for outdoor activities!")
        
        # Wind recommendations
        if wind_speed > 10:
            recommendations.append("💨 Windy conditions - secure loose items!")
        
        # Humidity recommendations
        if humidity > 70:
            recommendations.append("💧 High humidity - stay hydrated!")
        
        # UV recommendations
        if uv_index > 6:
            recommendations.append("☀️ High UV - use sunscreen and seek shade!")
        elif uv_index > 3:
            recommendations.append("☀️ Moderate UV - consider sunscreen!")
        
        return recommendations


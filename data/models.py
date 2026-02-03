"""
Data models for Weather Dashboard.

This module contains data classes and models for weather information
with proper type hints and serialization support.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class WeatherCondition:
    """
    Weather condition data model.
    
    Represents current weather conditions including temperature,
    humidity, wind, and weather description.
    """
    
    timestamp: float
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float  # Celsius
    feels_like: float  # Celsius
    temp_min: float  # Celsius
    temp_max: float  # Celsius
    pressure: int  # hPa
    humidity: int  # Percentage
    wind_speed: float  # m/s
    wind_deg: int  # Degrees
    cloudiness: int  # Percentage
    weather_main: str  # e.g., "Clear", "Rain"
    weather_description: str  # e.g., "clear sky"
    sunrise: int  # Unix timestamp
    sunset: int  # Unix timestamp
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert weather condition to dictionary.
        
        Returns:
            Dict[str, Any]: Weather data as dictionary.
        """
        return asdict(self)
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'WeatherCondition':
        """
        Create WeatherCondition from OpenWeatherMap API response.
        
        Args:
            data: API response data.
            
        Returns:
            WeatherCondition: Parsed weather condition object.
        """
        return cls(
            timestamp=data['dt'],
            city=data['name'],
            country=data['sys']['country'],
            latitude=data['coord']['lat'],
            longitude=data['coord']['lon'],
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            temp_min=data['main']['temp_min'],
            temp_max=data['main']['temp_max'],
            pressure=data['main']['pressure'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            wind_deg=data['wind'].get('deg', 0),
            cloudiness=data['clouds']['all'],
            weather_main=data['weather'][0]['main'],
            weather_description=data['weather'][0]['description'],
            sunrise=data['sys']['sunrise'],
            sunset=data['sys']['sunset']
        )
    
    def get_datetime(self) -> datetime:
        """
        Get timestamp as datetime object.
        
        Returns:
            datetime: Timestamp as datetime.
        """
        return datetime.fromtimestamp(self.timestamp)
    
    def get_weather_emoji(self) -> str:
        """
        Get emoji representation of weather condition.
        
        Returns:
            str: Weather emoji.
        """
        emoji_map = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️'
        }
        return emoji_map.get(self.weather_main, '🌤️')


@dataclass
class HistoricalWeatherData:
    """
    Historical weather data model.
    
    Stores multiple weather conditions for historical analysis.
    """
    
    location: str
    data_points: list[WeatherCondition]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert historical data to dictionary.
        
        Returns:
            Dict[str, Any]: Historical data as dictionary.
        """
        return {
            'location': self.location,
            'data_points': [dp.to_dict() for dp in self.data_points]
        }
    
    def get_average_temperature(self) -> float:
        """
        Calculate average temperature from historical data.
        
        Returns:
            float: Average temperature in Celsius.
        """
        if not self.data_points:
            return 0.0
        return sum(dp.temperature for dp in self.data_points) / len(self.data_points)
    
    def get_average_humidity(self) -> float:
        """
        Calculate average humidity from historical data.
        
        Returns:
            float: Average humidity percentage.
        """
        if not self.data_points:
            return 0.0
        return sum(dp.humidity for dp in self.data_points) / len(self.data_points)


@dataclass
class WeatherComparison:
    """
    Weather comparison result model.
    
    Contains comparison between current and historical weather conditions.
    """
    
    current: WeatherCondition
    historical_avg_temp: float
    historical_avg_humidity: float
    temp_difference: float
    humidity_difference: float
    trend: str  # "warmer", "cooler", "similar"
    
    def get_trend_indicator(self) -> str:
        """
        Get visual indicator for temperature trend.
        
        Returns:
            str: Trend indicator with emoji.
        """
        if self.temp_difference > 2:
            return f"🔥 {self.temp_difference:.1f}°C warmer than average"
        elif self.temp_difference < -2:
            return f"❄️ {abs(self.temp_difference):.1f}°C cooler than average"
        else:
            return f"➡️ Similar to average (±{abs(self.temp_difference):.1f}°C)"

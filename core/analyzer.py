"""
Weather comparison and analysis module.

This module contains business logic for comparing current weather
with historical data and calculating statistical trends.
"""

from typing import List, Optional
from data.models import WeatherCondition, WeatherComparison, HistoricalWeatherData


class WeatherAnalyzer:
    """
    Weather data analyzer.
    
    Performs statistical analysis and comparison of weather conditions
    including trend detection and average calculations.
    """
    
    def compare_weather(
        self,
        current: WeatherCondition,
        historical: List[WeatherCondition]
    ) -> WeatherComparison:
        """
        Compare current weather with historical data.
        
        Args:
            current: Current weather condition.
            historical: List of historical weather conditions.
            
        Returns:
            WeatherComparison: Comparison results.
        """
        if not historical:
            # No historical data available
            return WeatherComparison(
                current=current,
                historical_avg_temp=current.temperature,
                historical_avg_humidity=float(current.humidity),
                temp_difference=0.0,
                humidity_difference=0.0,
                trend="no_data"
            )
        
        # Calculate historical averages
        avg_temp = sum(h.temperature for h in historical) / len(historical)
        avg_humidity = sum(h.humidity for h in historical) / len(historical)
        
        # Calculate differences
        temp_diff = current.temperature - avg_temp
        humidity_diff = current.humidity - avg_humidity
        
        # Determine trend
        if temp_diff > 2:
            trend = "warmer"
        elif temp_diff < -2:
            trend = "cooler"
        else:
            trend = "similar"
        
        return WeatherComparison(
            current=current,
            historical_avg_temp=avg_temp,
            historical_avg_humidity=avg_humidity,
            temp_difference=temp_diff,
            humidity_difference=humidity_diff,
            trend=trend
        )
    
    def get_temperature_trend(
        self,
        weather_data: List[WeatherCondition]
    ) -> List[tuple[str, float]]:
        """
        Extract temperature trend from weather data.
        
        Args:
            weather_data: List of weather conditions sorted by time.
            
        Returns:
            List of (date, temperature) tuples.
        """
        from datetime import datetime
        
        trend = []
        for weather in weather_data:
            date_str = datetime.fromtimestamp(weather.timestamp).strftime('%Y-%m-%d')
            trend.append((date_str, weather.temperature))
        
        return trend
    
    def calculate_statistics(
        self,
        weather_data: List[WeatherCondition]
    ) -> dict:
        """
        Calculate statistical summary of weather data.
        
        Args:
            weather_data: List of weather conditions.
            
        Returns:
            Dictionary with statistical metrics.
        """
        if not weather_data:
            return {
                'count': 0,
                'avg_temp': 0.0,
                'min_temp': 0.0,
                'max_temp': 0.0,
                'avg_humidity': 0.0,
                'avg_wind_speed': 0.0
            }
        
        temps = [w.temperature for w in weather_data]
        humidities = [w.humidity for w in weather_data]
        wind_speeds = [w.wind_speed for w in weather_data]
        
        return {
            'count': len(weather_data),
            'avg_temp': sum(temps) / len(temps),
            'min_temp': min(temps),
            'max_temp': max(temps),
            'avg_humidity': sum(humidities) / len(humidities),
            'avg_wind_speed': sum(wind_speeds) / len(wind_speeds)
        }
    
    def detect_unusual_weather(
        self,
        current: WeatherCondition,
        historical: List[WeatherCondition]
    ) -> List[str]:
        """
        Detect unusual weather patterns.
        
        Args:
            current: Current weather condition.
            historical: Historical weather data.
            
        Returns:
            List of unusual weather indicators.
        """
        if not historical:
            return []
        
        unusual = []
        stats = self.calculate_statistics(historical)
        
        # Check temperature extremes
        if current.temperature > stats['max_temp']:
            unusual.append(f"🔥 Hottest temperature recorded ({current.temperature:.1f}°C)")
        elif current.temperature < stats['min_temp']:
            unusual.append(f"❄️ Coldest temperature recorded ({current.temperature:.1f}°C)")
        
        # Check humidity extremes
        if current.humidity > 90:
            unusual.append(f"💧 Very high humidity ({current.humidity}%)")
        elif current.humidity < 20:
            unusual.append(f"🏜️ Very low humidity ({current.humidity}%)")
        
        # Check wind speed
        if current.wind_speed > 15:
            unusual.append(f"💨 Strong winds ({current.wind_speed:.1f} m/s)")
        
        return unusual

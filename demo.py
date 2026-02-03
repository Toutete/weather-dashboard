#!/usr/bin/env python3
"""
Demo script for Weather Dashboard.

Demonstrates the application functionality without requiring a real API key.
Uses mock data to showcase all features.
"""

from datetime import datetime, timedelta
from data.models import WeatherCondition, WeatherComparison
from core.analyzer import WeatherAnalyzer
from ui.dashboard import WeatherDashboard


def create_mock_weather(city: str, temp: float, offset_days: int = 0) -> WeatherCondition:
    """Create mock weather data for demonstration."""
    timestamp = datetime.now() - timedelta(days=offset_days)
    
    return WeatherCondition(
        timestamp=timestamp.timestamp(),
        city=city,
        country="GB",
        latitude=51.51,
        longitude=-0.13,
        temperature=temp,
        feels_like=temp - 1,
        temp_min=temp - 2,
        temp_max=temp + 2,
        pressure=1013,
        humidity=65,
        wind_speed=3.5,
        wind_deg=220,
        cloudiness=10,
        weather_main="Clear",
        weather_description="clear sky",
        sunrise=1706950800,
        sunset=1706982400
    )


def run_demo():
    """Run weather dashboard demonstration."""
    print("\n" + "=" * 70)
    print("🌤️  WEATHER DASHBOARD DEMO")
    print("=" * 70 + "\n")
    
    dashboard = WeatherDashboard()
    analyzer = WeatherAnalyzer()
    
    # Create mock current weather
    dashboard.display_info("Creating demo weather data for London...")
    current_weather = create_mock_weather("London", 15.5)
    
    # Display current weather
    dashboard.display_current_weather(current_weather)
    
    # Create mock historical data
    dashboard.display_info("Generating historical data for past 7 days...")
    historical_data = [
        create_mock_weather("London", 12.0, 7),
        create_mock_weather("London", 11.5, 6),
        create_mock_weather("London", 13.0, 5),
        create_mock_weather("London", 14.0, 4),
        create_mock_weather("London", 12.5, 3),
        create_mock_weather("London", 13.5, 2),
        create_mock_weather("London", 14.5, 1),
    ]
    
    # Display historical trend
    dashboard.display_historical_trend(historical_data)
    
    # Compare with historical
    comparison = analyzer.compare_weather(current_weather, historical_data)
    dashboard.display_comparison(comparison)
    
    # Display statistics
    stats = analyzer.calculate_statistics(historical_data)
    dashboard.display_statistics(stats)
    
    # Detect unusual patterns (demo with extreme weather)
    extreme_weather = create_mock_weather("London", 25.0)  # Unusually warm
    extreme_weather.humidity = 95  # Very high humidity
    extreme_weather.wind_speed = 18.0  # Strong wind
    
    unusual = analyzer.detect_unusual_weather(extreme_weather, historical_data)
    if unusual:
        dashboard.display_unusual_patterns(unusual)
    
    dashboard.display_success("Demo completed!")
    
    print("\n" + "=" * 70)
    print("📖 To use with real data:")
    print("   1. Get API key from: https://openweathermap.org/api")
    print("   2. Copy .env.example to .env")
    print("   3. Add your API key to .env file")
    print("   4. Run: python main.py -c YourCity")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    run_demo()

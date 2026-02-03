#!/usr/bin/env python3
"""
Weather Dashboard Application.

Main entry point for the weather dashboard CLI application.
Orchestrates API calls, data storage, analysis, and display.
"""

import sys
import argparse
from typing import Optional

from config import config
from api.weather_client import WeatherAPIClient, WeatherAPIError
from data.storage import WeatherStorage
from core.analyzer import WeatherAnalyzer
from ui.dashboard import WeatherDashboard


class WeatherDashboardApp:
    """
    Main weather dashboard application.
    
    Coordinates between API client, storage, analyzer, and UI components
    to provide a complete weather dashboard experience.
    """
    
    def __init__(self):
        """Initialize application components."""
        self.config = config
        self.dashboard = WeatherDashboard()
        
        # Validate configuration
        if not self.config.validate():
            self.dashboard.display_error(
                "API key not configured. Please set OPENWEATHER_API_KEY in .env file."
            )
            self.dashboard.display_info(
                "Get your free API key from: https://openweathermap.org/api"
            )
            sys.exit(1)
        
        # Initialize components
        self.api_client = WeatherAPIClient(
            self.config.get_api_key(),
            self.config.current_weather_url
        )
        self.storage = WeatherStorage(
            self.config.storage_file,
            self.config.cache_duration_minutes
        )
        self.analyzer = WeatherAnalyzer()
    
    def run(self, city: Optional[str] = None, use_cache: bool = True) -> None:
        """
        Run the weather dashboard.
        
        Args:
            city: City name to fetch weather for. Uses default if None.
            use_cache: Whether to use cached data if available.
        """
        city = city or self.config.default_city
        
        try:
            # Try to use cached data first
            current_weather = None
            if use_cache:
                current_weather = self.storage.get_cached_weather(city)
                if current_weather:
                    self.dashboard.display_info(f"Using cached data for {city}")
            
            # Fetch fresh data if no cache or cache disabled
            if not current_weather:
                self.dashboard.display_info(f"Fetching current weather for {city}...")
                current_weather = self.api_client.get_current_weather(city)
                
                # Save to storage
                self.storage.save_weather_data(current_weather)
                self.dashboard.display_success("Weather data fetched successfully!")
            
            # Display current weather
            self.dashboard.display_current_weather(current_weather)
            
            # Get historical data
            historical_data = self.storage.get_recent_weather(
                current_weather.city,
                days=self.config.historical_days
            )
            
            # If we don't have enough historical data, simulate some
            if len(historical_data) < 3:
                self.dashboard.display_info(
                    "Insufficient historical data. Generating simulated data for demonstration..."
                )
                historical_data = self.api_client.simulate_historical_data(
                    current_weather.city,
                    days=self.config.historical_days
                )
                
                # Save simulated data
                for weather in historical_data:
                    self.storage.save_weather_data(weather)
            
            # Display historical trend
            if historical_data:
                self.dashboard.display_historical_trend(historical_data)
                
                # Compare with historical data
                comparison = self.analyzer.compare_weather(
                    current_weather,
                    historical_data
                )
                self.dashboard.display_comparison(comparison)
                
                # Display statistics
                stats = self.analyzer.calculate_statistics(historical_data)
                self.dashboard.display_statistics(stats)
                
                # Detect unusual patterns
                unusual = self.analyzer.detect_unusual_weather(
                    current_weather,
                    historical_data
                )
                if unusual:
                    self.dashboard.display_unusual_patterns(unusual)
            
        except WeatherAPIError as e:
            self.dashboard.display_error(str(e))
            sys.exit(1)
        except Exception as e:
            self.dashboard.display_error(f"Unexpected error: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Weather Dashboard - Display current and historical weather data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Use default city from config
  python main.py -c London          # Get weather for London
  python main.py -c "New York,US"   # Get weather for New York, US
  python main.py -c Paris --no-cache # Fetch fresh data without cache
        """
    )
    
    parser.add_argument(
        '-c', '--city',
        type=str,
        help='City name (e.g., "London" or "London,UK")'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable cache and fetch fresh data'
    )
    
    args = parser.parse_args()
    
    # Create and run application
    app = WeatherDashboardApp()
    app.run(city=args.city, use_cache=not args.no_cache)


if __name__ == '__main__':
    main()

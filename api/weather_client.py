"""
Weather API client module.

This module provides interface to OpenWeatherMap API for fetching
current and historical weather data.
"""

import requests
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from data.models import WeatherCondition


class WeatherAPIError(Exception):
    """Custom exception for Weather API errors."""
    pass


class WeatherAPIClient:
    """
    OpenWeatherMap API client.
    
    Handles API requests for current and historical weather data
    with proper error handling and rate limiting considerations.
    """
    
    def __init__(self, api_key: str, current_weather_url: str):
        """
        Initialize API client.
        
        Args:
            api_key: OpenWeatherMap API key.
            current_weather_url: Base URL for current weather API.
        """
        self.api_key = api_key
        self.current_weather_url = current_weather_url
        self.timeout = 10  # seconds
    
    def get_current_weather(self, city: str) -> WeatherCondition:
        """
        Fetch current weather data for a city.
        
        Args:
            city: City name (e.g., "London" or "London,UK").
            
        Returns:
            WeatherCondition: Current weather data.
            
        Raises:
            WeatherAPIError: If API request fails.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Use Celsius
        }
        
        try:
            response = requests.get(
                self.current_weather_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return WeatherCondition.from_api_response(data)
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError(f"Request timeout while fetching weather for {city}")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Network connection error. Please check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise WeatherAPIError("Invalid API key. Please check your configuration.")
            elif e.response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' not found. Please check the city name.")
            else:
                raise WeatherAPIError(f"API error: {e.response.status_code} - {e.response.text}")
        except (KeyError, ValueError) as e:
            raise WeatherAPIError(f"Error parsing API response: {str(e)}")
        except Exception as e:
            raise WeatherAPIError(f"Unexpected error: {str(e)}")
    
    def get_current_weather_by_coords(self, lat: float, lon: float) -> WeatherCondition:
        """
        Fetch current weather data by coordinates.
        
        Args:
            lat: Latitude.
            lon: Longitude.
            
        Returns:
            WeatherCondition: Current weather data.
            
        Raises:
            WeatherAPIError: If API request fails.
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(
                self.current_weather_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return WeatherCondition.from_api_response(data)
            
        except Exception as e:
            raise WeatherAPIError(f"Error fetching weather by coordinates: {str(e)}")
    
    def simulate_historical_data(
        self, 
        city: str, 
        days: int = 7
    ) -> List[WeatherCondition]:
        """
        Simulate historical weather data.
        
        Note: OpenWeatherMap's historical API requires paid subscription.
        This method simulates historical data by fetching current weather
        and creating variations for demonstration purposes.
        
        For production use with actual historical data, implement using
        the One Call API historical endpoint with a paid subscription.
        
        Args:
            city: City name.
            days: Number of days of historical data.
            
        Returns:
            List[WeatherCondition]: Simulated historical weather data.
        """
        # Fetch current weather as base
        current = self.get_current_weather(city)
        historical = []
        
        # Create simulated historical data points
        import random
        for i in range(days):
            # Simulate temperature variations
            temp_variation = random.uniform(-5, 5)
            humidity_variation = random.randint(-10, 10)
            
            # Create modified weather condition for past day
            timestamp = datetime.now() - timedelta(days=days-i)
            
            historical_weather = WeatherCondition(
                timestamp=timestamp.timestamp(),
                city=current.city,
                country=current.country,
                latitude=current.latitude,
                longitude=current.longitude,
                temperature=current.temperature + temp_variation,
                feels_like=current.feels_like + temp_variation,
                temp_min=current.temp_min + temp_variation - 2,
                temp_max=current.temp_max + temp_variation + 2,
                pressure=current.pressure + random.randint(-10, 10),
                humidity=max(0, min(100, current.humidity + humidity_variation)),
                wind_speed=current.wind_speed + random.uniform(-2, 2),
                wind_deg=current.wind_deg,
                cloudiness=max(0, min(100, current.cloudiness + random.randint(-20, 20))),
                weather_main=current.weather_main,
                weather_description=current.weather_description,
                sunrise=current.sunrise,
                sunset=current.sunset
            )
            historical.append(historical_weather)
        
        return historical

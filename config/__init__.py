"""
Configuration module for Weather Dashboard.

This module handles application configuration, API keys, and settings
loaded from environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class for Weather Dashboard application.
    
    Manages API keys, default settings, and application parameters
    loaded from environment variables.
    """
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.api_key: str = os.getenv('OPENWEATHER_API_KEY', '')
        self.default_city: str = os.getenv('DEFAULT_CITY', 'London')
        self.cache_duration_minutes: int = int(os.getenv('CACHE_DURATION_MINUTES', '30'))
        self.historical_days: int = int(os.getenv('HISTORICAL_DAYS', '7'))
        
        # API endpoints
        self.current_weather_url: str = 'https://api.openweathermap.org/data/2.5/weather'
        self.historical_weather_url: str = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
        self.onecall_url: str = 'https://api.openweathermap.org/data/2.5/onecall'
        
        # Storage settings
        self.data_dir: str = 'data'
        self.cache_dir: str = os.path.join(self.data_dir, 'cache')
        self.storage_file: str = os.path.join(self.data_dir, 'weather_history.json')
    
    def validate(self) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        if not self.api_key or self.api_key == 'your_api_key_here':
            return False
        return True
    
    def get_api_key(self) -> str:
        """
        Get the OpenWeatherMap API key.
        
        Returns:
            str: API key.
        """
        return self.api_key


# Global configuration instance
config = Config()

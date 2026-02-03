"""
Storage module for Weather Dashboard.

This module provides data persistence functionality using JSON files
for storing and retrieving weather data with caching support.
"""

import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from data.models import WeatherCondition


class WeatherStorage:
    """
    Weather data storage interface using JSON files.
    
    Manages persistent storage of weather data with caching capabilities
    to minimize API calls.
    """
    
    def __init__(self, storage_file: str, cache_duration_minutes: int = 30):
        """
        Initialize storage interface.
        
        Args:
            storage_file: Path to JSON storage file.
            cache_duration_minutes: Duration for which cached data is valid.
        """
        self.storage_file = storage_file
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self) -> None:
        """Create storage directory if it doesn't exist."""
        storage_dir = os.path.dirname(self.storage_file)
        if storage_dir and not os.path.exists(storage_dir):
            os.makedirs(storage_dir, exist_ok=True)
    
    def save_weather_data(self, weather: WeatherCondition) -> None:
        """
        Save weather data to storage.
        
        Args:
            weather: Weather condition to save.
        """
        data = self._load_all_data()
        
        # Add new weather data
        if weather.city not in data:
            data[weather.city] = []
        
        data[weather.city].append(weather.to_dict())
        
        # Keep only last 30 days of data per city
        self._cleanup_old_data(data, days=30)
        
        self._save_all_data(data)
    
    def get_recent_weather(self, city: str, days: int = 7) -> List[WeatherCondition]:
        """
        Retrieve recent weather data for a city.
        
        Args:
            city: City name.
            days: Number of days to retrieve.
            
        Returns:
            List[WeatherCondition]: List of weather conditions.
        """
        data = self._load_all_data()
        
        if city not in data:
            return []
        
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        recent_data = [
            WeatherCondition(**item)
            for item in data[city]
            if item['timestamp'] > cutoff_time
        ]
        
        # Sort by timestamp
        recent_data.sort(key=lambda x: x.timestamp)
        return recent_data
    
    def get_cached_weather(self, city: str) -> Optional[WeatherCondition]:
        """
        Get cached weather data if still valid.
        
        Args:
            city: City name.
            
        Returns:
            Optional[WeatherCondition]: Cached weather or None if expired.
        """
        recent = self.get_recent_weather(city, days=1)
        if not recent:
            return None
        
        latest = recent[-1]
        data_age = datetime.now() - latest.get_datetime()
        
        if data_age < self.cache_duration:
            return latest
        
        return None
    
    def _load_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load all data from storage file.
        
        Returns:
            Dict: All stored weather data.
        """
        if not os.path.exists(self.storage_file):
            return {}
        
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_all_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Save all data to storage file.
        
        Args:
            data: Data to save.
        """
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _cleanup_old_data(self, data: Dict[str, List[Dict[str, Any]]], days: int) -> None:
        """
        Remove data older than specified days.
        
        Args:
            data: Data dictionary to clean up.
            days: Number of days to keep.
        """
        cutoff_time = datetime.now().timestamp() - (days * 86400)
        
        for city in data:
            data[city] = [
                item for item in data[city]
                if item['timestamp'] > cutoff_time
            ]

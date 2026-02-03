#!/usr/bin/env python3
"""
Flask Web Application for Weather Dashboard.

Provides a mobile-friendly web interface and RESTful API endpoints
for accessing weather data.
"""

import os
from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from typing import Dict, Any, Optional

from config import config
from api.weather_client import WeatherAPIClient, WeatherAPIError
from data.storage import WeatherStorage
from core.analyzer import WeatherAnalyzer
from data.models import WeatherCondition


app = Flask(__name__)
CORS(app)  # Enable CORS for API endpoints

# Initialize components
api_client = None
storage = None
analyzer = None


def init_components():
    """Initialize weather dashboard components."""
    global api_client, storage, analyzer
    
    if not config.validate():
        print("⚠️  Warning: API key not configured. Set OPENWEATHER_API_KEY in .env file.")
        print("Get your free API key from: https://openweathermap.org/api")
        return False
    
    api_client = WeatherAPIClient(
        config.get_api_key(),
        config.current_weather_url
    )
    storage = WeatherStorage(
        config.storage_file,
        config.cache_duration_minutes
    )
    analyzer = WeatherAnalyzer()
    return True


def get_wind_direction_korean(degrees: int) -> str:
    """
    Convert wind direction degrees to Korean cardinal direction.
    
    Args:
        degrees: Wind direction in degrees (0-360).
        
    Returns:
        Korean cardinal direction string.
    """
    directions = ["북", "북동", "동", "남동", "남", "남서", "서", "북서"]
    idx = round(degrees / 45) % 8
    return directions[idx]


# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ 날씨 대시보드</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .search-box {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 25px;
        }
        
        .search-form {
            display: flex;
            gap: 10px;
        }
        
        .search-input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .search-button {
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .search-button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .search-button:active {
            transform: translateY(0);
        }
        
        .weather-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 25px;
            animation: slideUp 0.5s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .city-name {
            font-size: 2em;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .weather-main {
            text-align: center;
            margin: 30px 0;
        }
        
        .temperature {
            font-size: 4em;
            font-weight: 700;
            color: #667eea;
            margin: 10px 0;
        }
        
        .weather-description {
            font-size: 1.5em;
            color: #666;
            margin: 10px 0;
        }
        
        .weather-emoji {
            font-size: 4em;
            margin: 10px 0;
        }
        
        .weather-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .detail-item {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        
        .detail-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
        }
        
        .detail-value {
            font-size: 1.4em;
            font-weight: 700;
            color: #333;
        }
        
        .comparison-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: slideUp 0.6s ease-out;
        }
        
        .comparison-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .comparison-item {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 15px 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .comparison-label {
            font-size: 1em;
            color: #666;
        }
        
        .comparison-value {
            font-size: 1.2em;
            font-weight: 700;
            color: #667eea;
        }
        
        .trend-indicator {
            font-size: 1.5em;
            margin-left: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: white;
            font-size: 1.2em;
        }
        
        .spinner {
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: rgba(255, 107, 107, 0.95);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            text-align: center;
            animation: shake 0.5s;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            
            .temperature {
                font-size: 3em;
            }
            
            .weather-details {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .search-form {
                flex-direction: column;
            }
            
            .search-button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌤️ 날씨 대시보드</h1>
        </div>
        
        <div class="search-box">
            <form class="search-form" onsubmit="searchWeather(event)">
                <input 
                    type="text" 
                    id="cityInput" 
                    class="search-input" 
                    placeholder="도시 이름을 입력하세요 (예: Seoul, Tokyo, New York)"
                    value="Seoul"
                />
                <button type="submit" class="search-button">🔍 검색</button>
            </form>
        </div>
        
        <div id="loading" class="loading hidden">
            <div class="spinner"></div>
            <p>날씨 정보를 가져오는 중...</p>
        </div>
        
        <div id="error" class="error hidden"></div>
        
        <div id="weatherCard" class="weather-card hidden">
            <div class="city-name" id="cityName"></div>
            <div class="weather-main">
                <div class="weather-emoji" id="weatherEmoji"></div>
                <div class="temperature" id="temperature"></div>
                <div class="weather-description" id="weatherDescription"></div>
            </div>
            <div class="weather-details" id="weatherDetails"></div>
        </div>
        
        <div id="comparisonCard" class="comparison-card hidden">
            <div class="comparison-title">📊 과거 날씨 비교</div>
            <div id="comparisonContent"></div>
        </div>
    </div>
    
    <script>
        // Automatically search for Seoul on page load
        window.addEventListener('DOMContentLoaded', () => {
            searchWeather(new Event('submit'));
        });
        
        async function searchWeather(event) {
            event.preventDefault();
            
            const cityInput = document.getElementById('cityInput');
            const city = cityInput.value.trim();
            
            if (!city) {
                showError('도시 이름을 입력해주세요.');
                return;
            }
            
            showLoading();
            hideError();
            hideWeather();
            
            try {
                // Fetch current weather
                const weatherResponse = await fetch(`/api/weather/${encodeURIComponent(city)}`);
                
                if (!weatherResponse.ok) {
                    const errorData = await weatherResponse.json();
                    throw new Error(errorData.error || '날씨 정보를 가져올 수 없습니다.');
                }
                
                const weatherData = await weatherResponse.json();
                displayWeather(weatherData);
                
                // Fetch comparison data
                try {
                    const comparisonResponse = await fetch(`/api/compare/${encodeURIComponent(city)}`);
                    if (comparisonResponse.ok) {
                        const comparisonData = await comparisonResponse.json();
                        displayComparison(comparisonData);
                    }
                } catch (error) {
                    console.log('Comparison data not available:', error);
                }
                
                hideLoading();
            } catch (error) {
                hideLoading();
                showError(error.message);
            }
        }
        
        function displayWeather(data) {
            const weatherCard = document.getElementById('weatherCard');
            const cityName = document.getElementById('cityName');
            const weatherEmoji = document.getElementById('weatherEmoji');
            const temperature = document.getElementById('temperature');
            const weatherDescription = document.getElementById('weatherDescription');
            const weatherDetails = document.getElementById('weatherDetails');
            
            cityName.textContent = `${data.city}, ${data.country}`;
            weatherEmoji.textContent = data.weather_emoji;
            temperature.textContent = `${Math.round(data.temperature)}°C`;
            weatherDescription.textContent = data.weather_description;
            
            weatherDetails.innerHTML = `
                <div class="detail-item">
                    <div class="detail-label">체감 온도</div>
                    <div class="detail-value">${Math.round(data.feels_like)}°C</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">습도</div>
                    <div class="detail-value">${data.humidity}%</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">풍속</div>
                    <div class="detail-value">${(data.wind_speed || 0).toFixed(1)} m/s</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">풍향</div>
                    <div class="detail-value">${data.wind_direction_korean || 'N/A'}</div>
                </div>
            `;
            
            weatherCard.classList.remove('hidden');
        }
        
        function displayComparison(data) {
            const comparisonCard = document.getElementById('comparisonCard');
            const comparisonContent = document.getElementById('comparisonContent');
            
            if (!data || !data.comparison) {
                comparisonCard.classList.add('hidden');
                return;
            }
            
            const comp = data.comparison;
            const tempDiff = comp.temp_difference;
            const trendEmoji = tempDiff > 2 ? '🔥' : tempDiff < -2 ? '❄️' : '➡️';
            const trendText = tempDiff > 2 ? '평균보다 따뜻함' : tempDiff < -2 ? '평균보다 추움' : '평균과 비슷함';
            
            comparisonContent.innerHTML = `
                <div class="comparison-item">
                    <span class="comparison-label">7일 평균 기온</span>
                    <span class="comparison-value">${(comp.historical_avg_temp || 0).toFixed(1)}°C</span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">현재 vs 평균</span>
                    <span class="comparison-value">
                        ${Math.abs(tempDiff || 0).toFixed(1)}°C ${tempDiff > 0 ? '높음' : '낮음'}
                        <span class="trend-indicator">${trendEmoji}</span>
                    </span>
                </div>
                <div class="comparison-item">
                    <span class="comparison-label">온도 트렌드</span>
                    <span class="comparison-value">${trendText}</span>
                </div>
            `;
            
            if (data.unusual_patterns && data.unusual_patterns.length > 0) {
                const unusualHtml = data.unusual_patterns.map(pattern => `
                    <div class="comparison-item">
                        <span class="comparison-label">특이 기상</span>
                        <span class="comparison-value" style="font-size: 1em;">${pattern}</span>
                    </div>
                `).join('');
                comparisonContent.innerHTML += unusualHtml;
            }
            
            comparisonCard.classList.remove('hidden');
        }
        
        function showLoading() {
            document.getElementById('loading').classList.remove('hidden');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.add('hidden');
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = `❌ ${message}`;
            errorDiv.classList.remove('hidden');
        }
        
        function hideError() {
            document.getElementById('error').classList.add('hidden');
        }
        
        function hideWeather() {
            document.getElementById('weatherCard').classList.add('hidden');
            document.getElementById('comparisonCard').classList.add('hidden');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render main web page."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/weather/<city>')
def get_weather(city: str):
    """
    Get current weather for a city.
    
    Args:
        city: City name.
        
    Returns:
        JSON response with weather data.
    """
    try:
        if not api_client:
            return jsonify({'error': 'API not configured'}), 500
        
        # Try to get cached data first
        cached = storage.get_cached_weather(city)
        if cached:
            weather = cached
        else:
            # Fetch fresh data
            weather = api_client.get_current_weather(city)
            storage.save_weather_data(weather)
        
        # Convert to JSON-serializable format
        result = {
            'city': weather.city,
            'country': weather.country,
            'temperature': weather.temperature,
            'feels_like': weather.feels_like,
            'temp_min': weather.temp_min,
            'temp_max': weather.temp_max,
            'humidity': weather.humidity,
            'pressure': weather.pressure,
            'wind_speed': weather.wind_speed,
            'wind_deg': weather.wind_deg,
            'wind_direction_korean': get_wind_direction_korean(weather.wind_deg),
            'cloudiness': weather.cloudiness,
            'weather_main': weather.weather_main,
            'weather_description': weather.weather_description,
            'weather_emoji': weather.get_weather_emoji(),
            'timestamp': weather.timestamp
        }
        
        return jsonify(result)
        
    except WeatherAPIError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500


@app.route('/api/history/<city>')
def get_history(city: str):
    """
    Get historical weather data for a city.
    
    Args:
        city: City name.
        
    Returns:
        JSON response with historical weather data.
    """
    try:
        if not storage:
            return jsonify({'error': 'Storage not configured'}), 500
        
        days = request.args.get('days', default=7, type=int)
        
        # Validate days parameter
        if days < 1 or days > 30:
            return jsonify({'error': 'Days must be between 1 and 30'}), 400
        
        historical = storage.get_recent_weather(city, days=days)
        
        # If insufficient historical data, simulate some
        if len(historical) < 3:
            current = api_client.get_current_weather(city)
            historical = api_client.simulate_historical_data(city, days=days)
            # Save simulated data
            for weather in historical:
                storage.save_weather_data(weather)
        
        result = [
            {
                'timestamp': w.timestamp,
                'temperature': w.temperature,
                'humidity': w.humidity,
                'weather_main': w.weather_main,
                'weather_description': w.weather_description
            }
            for w in historical
        ]
        
        return jsonify({'history': result, 'count': len(result)})
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500


@app.route('/api/compare/<city>')
def get_comparison(city: str):
    """
    Get weather comparison between current and historical data.
    
    Args:
        city: City name.
        
    Returns:
        JSON response with comparison data.
    """
    try:
        if not api_client or not storage or not analyzer:
            return jsonify({'error': 'Components not configured'}), 500
        
        # Get current weather
        current = api_client.get_current_weather(city)
        
        # Get historical data
        historical = storage.get_recent_weather(city, days=config.historical_days)
        
        # If insufficient historical data, simulate some
        if len(historical) < 3:
            historical = api_client.simulate_historical_data(city, days=config.historical_days)
            for weather in historical:
                storage.save_weather_data(weather)
        
        # Perform comparison
        comparison = analyzer.compare_weather(current, historical)
        
        # Detect unusual patterns
        unusual = analyzer.detect_unusual_weather(current, historical)
        
        result = {
            'comparison': {
                'historical_avg_temp': comparison.historical_avg_temp,
                'historical_avg_humidity': comparison.historical_avg_humidity,
                'temp_difference': comparison.temp_difference,
                'humidity_difference': comparison.humidity_difference,
                'trend': comparison.trend
            },
            'unusual_patterns': unusual
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Main entry point for web application."""
    print("=" * 60)
    print("🌤️  Weather Dashboard Web Application")
    print("=" * 60)
    
    if not init_components():
        print("\n❌ Failed to initialize components.")
        print("Please configure your API key in .env file.")
        return
    
    print("\n✅ Components initialized successfully!")
    print("\n📱 Starting web server...")
    print("\n🌐 Access the dashboard at:")
    print("   - Local:   http://localhost:5000")
    print("   - Network: http://<your-ip>:5000")
    print("\n💡 Tips:")
    print("   - Find your IP: Run 'ipconfig' (Windows) or 'ifconfig' (Mac/Linux)")
    print("   - Mobile access: Connect to same WiFi and use Network URL")
    print("   - Press Ctrl+C to stop the server")
    print("\n" + "=" * 60 + "\n")
    
    # Run Flask app
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(
        host='0.0.0.0',  # Listen on all interfaces for mobile access
        port=5000,
        debug=debug_mode
    )


if __name__ == '__main__':
    main()

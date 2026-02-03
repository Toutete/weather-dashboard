# Weather Dashboard 🌤️

A comprehensive Python weather dashboard application that fetches real-time weather data from OpenWeatherMap API, compares it with historical data, and displays beautiful visualizations in your terminal.

## Features ✨

- 🌡️ **Current Weather Display**: Real-time temperature, humidity, wind speed, and weather conditions
- 📊 **Historical Comparison**: Compare current weather with past 7 days average
- 📈 **Temperature Trends**: Visualize weather patterns over time
- 💾 **Smart Caching**: Reduces API calls by caching recent data
- 🎨 **Rich CLI Interface**: Beautiful terminal output with colors and emojis
- ⚠️ **Unusual Pattern Detection**: Highlights extreme weather conditions
- 🌍 **Location Search**: Search by city name or coordinates

## Architecture Overview 🏗️

The application follows **Clean Architecture** principles with clear separation of concerns:

```
weather-dashboard/
├── config/              # Configuration Layer
│   └── __init__.py     # API keys, settings, environment variables
├── api/                 # API Layer
│   └── weather_client.py  # OpenWeatherMap API client
├── data/                # Data Layer
│   ├── models.py       # Weather data models with type hints
│   └── storage.py      # JSON-based storage and caching
├── core/                # Business Logic Layer
│   └── analyzer.py     # Weather comparison and statistical analysis
├── ui/                  # Presentation Layer
│   └── dashboard.py    # CLI interface with rich formatting
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # Documentation
```

### Component Responsibilities

#### 1. Configuration Layer (`config/`)
- **Purpose**: Centralized configuration management
- **Responsibilities**:
  - Load API keys from environment variables
  - Manage application settings (cache duration, default city, etc.)
  - Validate configuration before application starts
  - Provide configuration interface to other components

#### 2. API Layer (`api/`)
- **Purpose**: External API communication
- **Responsibilities**:
  - Fetch current weather data from OpenWeatherMap API
  - Handle API authentication and request formation
  - Error handling for network failures and API errors
  - Parse and validate API responses
  - Simulate historical data (free tier limitation workaround)

#### 3. Data Layer (`data/`)
- **Purpose**: Data persistence and modeling
- **Responsibilities**:
  - Define weather data models with type hints (`models.py`)
  - Store and retrieve weather data from JSON files (`storage.py`)
  - Implement caching mechanism to reduce API calls
  - Manage data serialization/deserialization
  - Clean up old data automatically

#### 4. Business Logic Layer (`core/`)
- **Purpose**: Weather analysis and computations
- **Responsibilities**:
  - Compare current weather with historical averages
  - Calculate statistical metrics (min, max, average)
  - Detect temperature trends (warmer/cooler)
  - Identify unusual weather patterns
  - Generate trend indicators

#### 5. Presentation Layer (`ui/`)
- **Purpose**: User interface and data visualization
- **Responsibilities**:
  - Format weather data for display
  - Render rich CLI output with colors and emojis
  - Create tables and panels for organized information
  - Display error and success messages
  - Provide visual indicators for weather conditions

#### 6. Application Entry Point (`main.py`)
- **Purpose**: Application orchestration
- **Responsibilities**:
  - Initialize all components
  - Parse command-line arguments
  - Coordinate data flow between layers
  - Handle application lifecycle
  - Manage error handling at top level

### Data Flow 🔄

```
User Input (CLI)
    ↓
main.py (Orchestrator)
    ↓
config/ (Load Configuration)
    ↓
api/ (Fetch Weather Data) → data/storage.py (Cache/Store)
    ↓
core/ (Analyze & Compare)
    ↓
ui/ (Format & Display)
    ↓
Terminal Output
```

### Design Patterns Used

1. **Singleton Pattern**: Configuration object (`config.config`)
2. **Repository Pattern**: `WeatherStorage` abstracts data persistence
3. **Strategy Pattern**: Different analysis strategies in `WeatherAnalyzer`
4. **Factory Pattern**: `WeatherCondition.from_api_response()` for object creation

## Setup Instructions 🚀

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenWeatherMap API key (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/Toutete/weather-dashboard.git
cd weather-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `rich`: Beautiful terminal formatting

### 3. Obtain API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

**`.env` file contents:**
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
DEFAULT_CITY=London
CACHE_DURATION_MINUTES=30
HISTORICAL_DAYS=7

# Optional: Flask web app debug mode (set to true for development)
FLASK_DEBUG=false
```

## Usage Examples 📖

### CLI (Command Line Interface)

The traditional command-line interface for terminal users.

```bash
# Use default city from configuration
python main.py

# Specify a city
python main.py -c "London"

# Use city with country code
python main.py -c "New York,US"

# Force fresh data (bypass cache)
python main.py -c "Paris" --no-cache
```

### Command-Line Options

```
Options:
  -h, --help            Show help message
  -c CITY, --city CITY  City name (e.g., "London" or "London,UK")
  --no-cache            Disable cache and fetch fresh data
```

### Sample Output

```
ℹ️  Fetching current weather for London...

✅ Weather data fetched successfully!

╭─────────────────── Current Weather ───────────────────╮
│                                                        │
│ Location: London, GB                                   │
│ Coordinates: 51.51, -0.13                             │
│ Time: 2026-02-03 14:30:15                             │
│                                                        │
│ ☀️ Clear - clear sky                                  │
│                                                        │
│ Temperature:                                           │
│   • Current: 12.5°C (feels like 11.2°C)               │
│   • Min/Max: 10.0°C / 14.5°C                          │
│                                                        │
│ Conditions:                                            │
│   • Humidity: 65%                                      │
│   • Pressure: 1013 hPa                                │
│   • Wind: 3.5 m/s at 220°                             │
│   • Cloudiness: 10%                                    │
╰────────────────────────────────────────────────────────╯
```

## Module Documentation 📚

### `config/__init__.py`
Manages application configuration from environment variables. Provides validation and centralized access to settings.

### `api/weather_client.py`
**Class**: `WeatherAPIClient`
- `get_current_weather(city)`: Fetch current weather for a city
- `get_current_weather_by_coords(lat, lon)`: Fetch weather by coordinates
- `simulate_historical_data(city, days)`: Generate simulated historical data

### `data/models.py`
**Classes**:
- `WeatherCondition`: Current weather data model
- `HistoricalWeatherData`: Historical weather collection
- `WeatherComparison`: Comparison results model

### `data/storage.py`
**Class**: `WeatherStorage`
- `save_weather_data(weather)`: Persist weather data
- `get_recent_weather(city, days)`: Retrieve historical data
- `get_cached_weather(city)`: Get cached data if valid

### `core/analyzer.py`
**Class**: `WeatherAnalyzer`
- `compare_weather(current, historical)`: Compare weather conditions
- `get_temperature_trend(weather_data)`: Extract temperature trend
- `calculate_statistics(weather_data)`: Statistical summary
- `detect_unusual_weather(current, historical)`: Detect extremes

### `ui/dashboard.py`
**Class**: `WeatherDashboard`
- `display_current_weather(weather)`: Show current conditions
- `display_comparison(comparison)`: Show comparison results
- `display_historical_trend(weather_data)`: Show trend table
- `display_statistics(stats)`: Show statistical summary

## Extensibility 🔧

### Adding New Weather Providers

1. Create a new client in `api/` directory
2. Implement the same interface as `WeatherAPIClient`
3. Update configuration to support multiple providers
4. Modify `main.py` to select provider based on config

### Adding New Visualization Types

1. Add methods to `ui/dashboard.py`
2. Use rich library features (charts, progress bars, etc.)
3. Call from `main.py` orchestration logic

### Adding Database Support

1. Create new storage class in `data/` implementing same interface
2. Add SQLite/PostgreSQL dependencies to `requirements.txt`
3. Update configuration to choose storage backend

## Error Handling 🛡️

The application handles:
- ❌ Invalid API keys
- ❌ Network connection failures
- ❌ API rate limiting
- ❌ Invalid city names
- ❌ Malformed API responses
- ❌ File system errors

All errors are displayed with clear, actionable messages.

## Limitations & Notes 📝

1. **Historical Data**: Free OpenWeatherMap tier doesn't include historical weather API. The application simulates historical data for demonstration purposes. For production use with real historical data, upgrade to a paid plan.

2. **API Rate Limits**: Free tier has 60 calls/minute and 1,000,000 calls/month. The caching mechanism helps stay within limits.

3. **Cache Duration**: Default 30 minutes. Adjust `CACHE_DURATION_MINUTES` in `.env` as needed.

## Web Application 🌐

### Overview

The Weather Dashboard now includes a **mobile-friendly web interface** that provides an elegant, responsive way to check weather information from any device!

### Features

- 📱 **Mobile-First Design**: Optimized for smartphones, tablets, and desktops
- 🎨 **Modern UI**: Beautiful gradient backgrounds and glass-morphism effects
- ⚡ **Real-time Data**: Instant weather updates via RESTful API
- 📊 **Historical Comparison**: Compare current weather with 7-day averages
- 🌡️ **Detailed Information**: Temperature, humidity, wind speed, and direction
- 🔍 **Smart Search**: City search with Enter key support
- 🎭 **Weather Emojis**: Visual weather condition indicators
- 📈 **Trend Analysis**: Temperature trends and unusual pattern detection

### Quick Start

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The web application requires Flask and Flask-CORS (automatically included in `requirements.txt`).

#### 2. Configure API Key

Make sure your `.env` file is set up with your OpenWeatherMap API key:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

#### 3. Run the Web Server

```bash
python web_app.py
```

#### 4. Access the Dashboard

**On the same computer:**
```
http://localhost:5000
```

**From mobile devices (same WiFi network):**
```
http://<your-computer-ip>:5000
```

### Finding Your Computer's IP Address

**Windows:**
```bash
ipconfig
# Look for "IPv4 Address" under your active network adapter
```

**Mac/Linux:**
```bash
ifconfig
# Look for "inet" address under your active network adapter (usually en0 or wlan0)
```

Or on Mac:
```bash
ipconfig getifaddr en0
```

**Example:**
If your IP is `192.168.1.100`, access from mobile at: `http://192.168.1.100:5000`

### Using the Web Interface

1. **Search for a City**: Enter any city name (e.g., "Seoul", "Tokyo", "New York")
2. **Press Enter or Click Search**: Weather data loads instantly
3. **View Current Weather**: 
   - Large temperature display
   - Weather emoji and description
   - Feels-like temperature
   - Humidity percentage
   - Wind speed and direction (in Korean!)
4. **Compare with History**: Automatically shows comparison with 7-day average
5. **Unusual Patterns**: Alerts for extreme weather conditions

### API Endpoints

The web application exposes RESTful API endpoints:

#### Get Current Weather
```http
GET /api/weather/<city>
```

**Example Response:**
```json
{
  "city": "Seoul",
  "country": "KR",
  "temperature": 15.5,
  "feels_like": 14.2,
  "humidity": 65,
  "wind_speed": 3.5,
  "wind_direction_korean": "북동",
  "weather_emoji": "☀️",
  "weather_description": "clear sky"
}
```

#### Get Historical Data
```http
GET /api/history/<city>?days=7
```

#### Get Weather Comparison
```http
GET /api/compare/<city>
```

**Example Response:**
```json
{
  "comparison": {
    "historical_avg_temp": 13.2,
    "temp_difference": 2.3,
    "trend": "warmer"
  },
  "unusual_patterns": [
    "🔥 Hottest temperature recorded (15.5°C)"
  ]
}
```

### Mobile Access Tips

1. **Same WiFi Network**: Ensure your phone and computer are on the same WiFi network
2. **Firewall**: You may need to allow Python/Flask through your firewall
3. **Add to Home Screen**: 
   - **iOS**: Safari → Share → "Add to Home Screen"
   - **Android**: Chrome → Menu → "Add to Home screen"
4. **Bookmark**: Save the URL for quick access

### Technology Stack

- **Backend**: Flask 3.0+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: CSS Grid, Flexbox, CSS Animations
- **Design**: Mobile-first responsive design
- **API**: RESTful architecture
- **CORS**: Enabled for cross-origin requests

### Design Highlights

- 🎨 **Gradient Background**: Purple-to-blue gradient for modern look
- 💎 **Glass-morphism**: Semi-transparent cards with backdrop blur
- ✨ **Animations**: Smooth fade-in and slide-up transitions
- 📱 **Responsive Grid**: Adapts to any screen size
- 🎯 **Touch-Friendly**: Large buttons and inputs for mobile
- 🌈 **Color Scheme**: #667eea primary color with thoughtful accents

### Troubleshooting Web App

#### Cannot access from mobile
- Verify both devices are on same WiFi network
- Check firewall settings allow incoming connections on port 5000
- Try using your computer's IP address instead of localhost
- Ensure web server is running (check terminal for "Running on...")

#### "API not configured" error
- Make sure `.env` file exists with valid `OPENWEATHER_API_KEY`
- Restart the web server after adding API key

#### Slow response times
- First request may be slower (API call)
- Subsequent requests use cached data (30-minute cache)
- Check your internet connection

## Troubleshooting 🔍

### "Invalid API key" error
- Verify your API key in `.env` file
- Check for extra spaces or quotes
- Ensure key is activated (can take a few hours after registration)

### "City not found" error
- Check city name spelling
- Try adding country code: "London,UK"
- Use exact name from OpenWeatherMap

### No historical data displayed
- Application needs to run multiple times over several days to collect real data
- Currently uses simulated data for immediate demonstration

## Contributing 🤝

Contributions are welcome! Areas for improvement:
- Implement charts using matplotlib/plotly
- Add support for multiple weather APIs
- Implement SQLite database storage
- Add unit tests
- Support for coordinates-based search in CLI
- Dark mode toggle for web interface
- PWA (Progressive Web App) features
- Favorite cities with localStorage

## License 📄

This project is open source and available for educational purposes.

## Acknowledgments 🙏

- OpenWeatherMap for providing free weather API
- Rich library for beautiful terminal output
- Python community for excellent tooling





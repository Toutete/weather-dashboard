"""
CLI Dashboard for Weather Application.

This module provides a command-line interface for displaying weather
information with rich formatting and visual indicators.
"""

from typing import List, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box
from data.models import WeatherCondition, WeatherComparison


class WeatherDashboard:
    """
    Weather dashboard CLI interface.
    
    Provides formatted display of weather information using
    rich library for enhanced terminal output.
    """
    
    def __init__(self):
        """Initialize dashboard with rich console."""
        self.console = Console()
    
    def display_current_weather(self, weather: WeatherCondition) -> None:
        """
        Display current weather information.
        
        Args:
            weather: Current weather condition.
        """
        emoji = weather.get_weather_emoji()
        
        # Create weather info panel
        weather_info = f"""
[bold cyan]Location:[/bold cyan] {weather.city}, {weather.country}
[bold cyan]Coordinates:[/bold cyan] {weather.latitude:.2f}, {weather.longitude:.2f}
[bold cyan]Time:[/bold cyan] {weather.get_datetime().strftime('%Y-%m-%d %H:%M:%S')}

{emoji} [bold yellow]{weather.weather_main}[/bold yellow] - {weather.weather_description}

[bold]Temperature:[/bold]
  • Current: [bold green]{weather.temperature:.1f}°C[/bold green] (feels like {weather.feels_like:.1f}°C)
  • Min/Max: {weather.temp_min:.1f}°C / {weather.temp_max:.1f}°C

[bold]Conditions:[/bold]
  • Humidity: {weather.humidity}%
  • Pressure: {weather.pressure} hPa
  • Wind: {weather.wind_speed:.1f} m/s at {weather.wind_deg}°
  • Cloudiness: {weather.cloudiness}%

[bold]Sun:[/bold]
  • Sunrise: {datetime.fromtimestamp(weather.sunrise).strftime('%H:%M:%S')}
  • Sunset: {datetime.fromtimestamp(weather.sunset).strftime('%H:%M:%S')}
        """
        
        panel = Panel(
            weather_info.strip(),
            title="[bold blue]Current Weather[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(panel)
    
    def display_comparison(self, comparison: WeatherComparison) -> None:
        """
        Display weather comparison with historical data.
        
        Args:
            comparison: Weather comparison results.
        """
        trend_indicator = comparison.get_trend_indicator()
        
        comparison_info = f"""
[bold]Current Temperature:[/bold] {comparison.current.temperature:.1f}°C
[bold]Historical Average:[/bold] {comparison.historical_avg_temp:.1f}°C

{trend_indicator}

[bold]Humidity Comparison:[/bold]
  • Current: {comparison.current.humidity}%
  • Average: {comparison.historical_avg_humidity:.1f}%
  • Difference: {comparison.humidity_difference:+.1f}%
        """
        
        panel = Panel(
            comparison_info.strip(),
            title="[bold magenta]Weather Comparison[/bold magenta]",
            border_style="magenta",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(panel)
    
    def display_historical_trend(
        self,
        weather_data: List[WeatherCondition]
    ) -> None:
        """
        Display historical weather trend as a table.
        
        Args:
            weather_data: List of historical weather conditions.
        """
        if not weather_data:
            self.console.print("[yellow]No historical data available.[/yellow]")
            return
        
        table = Table(
            title="Historical Weather Trend (Last 7 Days)",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Date", style="cyan", justify="center")
        table.add_column("Weather", style="yellow", justify="center")
        table.add_column("Temp (°C)", style="green", justify="right")
        table.add_column("Humidity (%)", style="blue", justify="right")
        table.add_column("Wind (m/s)", style="magenta", justify="right")
        
        for weather in weather_data:
            date_str = weather.get_datetime().strftime('%Y-%m-%d')
            emoji = weather.get_weather_emoji()
            
            table.add_row(
                date_str,
                f"{emoji} {weather.weather_main}",
                f"{weather.temperature:.1f}",
                f"{weather.humidity}",
                f"{weather.wind_speed:.1f}"
            )
        
        self.console.print()
        self.console.print(table)
    
    def display_statistics(self, stats: dict) -> None:
        """
        Display statistical summary.
        
        Args:
            stats: Statistics dictionary.
        """
        stats_info = f"""
[bold]Temperature:[/bold]
  • Average: {stats['avg_temp']:.1f}°C
  • Minimum: {stats['min_temp']:.1f}°C
  • Maximum: {stats['max_temp']:.1f}°C

[bold]Other Metrics:[/bold]
  • Average Humidity: {stats['avg_humidity']:.1f}%
  • Average Wind Speed: {stats['avg_wind_speed']:.1f} m/s
  • Data Points: {stats['count']}
        """
        
        panel = Panel(
            stats_info.strip(),
            title="[bold green]Statistical Summary[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(panel)
    
    def display_unusual_patterns(self, patterns: List[str]) -> None:
        """
        Display unusual weather patterns.
        
        Args:
            patterns: List of unusual weather indicators.
        """
        if not patterns:
            return
        
        patterns_text = "\n".join(f"  • {pattern}" for pattern in patterns)
        
        panel = Panel(
            patterns_text,
            title="[bold red]⚠️  Unusual Weather Patterns[/bold red]",
            border_style="red",
            box=box.ROUNDED
        )
        
        self.console.print()
        self.console.print(panel)
    
    def display_error(self, message: str) -> None:
        """
        Display error message.
        
        Args:
            message: Error message to display.
        """
        self.console.print(f"\n[bold red]❌ Error:[/bold red] {message}\n")
    
    def display_info(self, message: str) -> None:
        """
        Display info message.
        
        Args:
            message: Info message to display.
        """
        self.console.print(f"\n[bold blue]ℹ️  {message}[/bold blue]\n")
    
    def display_success(self, message: str) -> None:
        """
        Display success message.
        
        Args:
            message: Success message to display.
        """
        self.console.print(f"\n[bold green]✅ {message}[/bold green]\n")

#!/usr/bin/env python3

import random
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Create the FastMCP server instance
mcp = FastMCP("WeatherServer")

# Mock weather data for different locations
WEATHER_DATA = {
    "Witham": {"temperature": 15.5, "condition": "partly cloudy", "humidity": 65},
    "Toronto": {"temperature": -2.3, "condition": "snow", "humidity": 80},
    "Plovdiv": {"temperature": 22.1, "condition": "sunny", "humidity": 45},
    "Southend-on-sea": {"temperature": 12.8, "condition": "rainy", "humidity": 85},
}

@mcp.tool()
def get_weather(location: str) -> str:
    """Get current weather information for a specific location.
    
    Args:
        location: The location to get weather for
        
    Returns:
        Weather information as a formatted string
    """
    if not location or not location.strip():
        return "Error: Location parameter is required"
    
    location = location.strip()
    
    # Check if we have weather data for this location
    if location in WEATHER_DATA:
        weather = WEATHER_DATA[location]
        result = {
            "location": location,
            "temperature": weather["temperature"],
            "condition": weather["condition"],
            "humidity": weather["humidity"]
        }
    else:
        # Generate random weather for unknown locations
        result = {
            "location": location,
            "temperature": round(random.uniform(-10, 35), 1),
            "condition": random.choice(["sunny", "cloudy", "rainy", "snow", "foggy"]),
            "humidity": random.randint(30, 90)
        }
    
    return f"Weather in {result['location']}: {result['temperature']}°C, {result['condition']}, humidity {result['humidity']}%"

@mcp.tool()
def get_random_weather() -> str:
    """Get weather information for a random location.
    
    Returns:
        Weather information for a random location as a formatted string
    """
    # Pick a random location from our known locations
    location = random.choice(list(WEATHER_DATA.keys()))
    weather = WEATHER_DATA[location]
    
    result = {
        "location": location,
        "temperature": weather["temperature"],
        "condition": weather["condition"],
        "humidity": weather["humidity"]
    }
    
    return f"Weather in {result['location']}: {result['temperature']}°C, {result['condition']}, humidity {result['humidity']}%"

if __name__ == "__main__":
    mcp.run()

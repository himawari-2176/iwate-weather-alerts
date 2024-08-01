import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": [39.7826, 39.7625, 39.6954, 39.7036, 39.5481, 39.5338, 39.6678, 39.3874, 39.476, 39.3258, 39.3622, 39.387, 39.3312, 39.1931, 39.286, 39.4342, 39.2758, 38.7208, 39.3039, 39.1975, 38.9783, 39.0816, 38.9336, 39.0825, 38.9341, 38.8701],
    "longitude": [140.9566, 141.0959, 140.9721, 141.1527, 141.1875, 141.7453, 141.1543, 141.1161, 141.2723, 141.4712, 141.9033, 140.6853, 141.5319, 141.1151, 141.1225, 141.7369, 141.869, 141.02, 141.13, 141.4317, 140.9439, 141.141, 141.2251, 141.7126, 141.1267, 141.2533],
    "current": ["precipitation", "wind_speed_10m"],
    "timezone": "Asia/Tokyo",
    "forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process all locations
for response in responses:
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_precipitation = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()

    print(f"Current time {current.Time()}")
    print(f"Current precipitation {current_precipitation}")
    print(f"Current wind_speed_10m {current_wind_speed_10m}")
    print()  # Add a newline for better readability between locations

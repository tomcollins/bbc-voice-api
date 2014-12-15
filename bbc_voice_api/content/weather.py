import requests

feed_url = 'http://open.live.bbc.co.uk/weather/feeds/en/%s/location-weather.json'

def fetch_forecasts(location_id):
    response = requests.get(feed_url % (location_id))
    weather_data = response.json

    forecasts = []
    is_first = True
    forecast_data = weather_data['forecasts']
    for day_data in forecast_data:
        day = day_data['summary']['report']
        forecasts.append({
            'temperature': {
                'high': { 'c': temperature_high_c, 'f': temperature_high_f },
                'low': { 'c': temperature_low_c, 'f': temperature_low_c }
            },
            'wind': {
                'speed': {}
            }
        })





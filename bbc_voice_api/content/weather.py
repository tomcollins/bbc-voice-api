import os
import requests
import requests_cache
from datetime import datetime

data_path = os.path.realpath(os.path.dirname(__file__) + '/../../data/')
requests_cache.install_cache(data_path + '/cache/voice_cache', expire_after=300)

feed_url = 'http://open.live.bbc.co.uk/weather/feeds/en/%s/location-weather.json'

def fetch_forecasts(location_id):
    response = requests.get(feed_url % (location_id))
    weather_data = response.json()

    forecasts = []
    is_first = True
    is_night = weather_data['night']
    location_data = weather_data['location']
    location = location_data['name']
    forecast_data = weather_data['forecasts']
    for day_data in forecast_data:
        day = day_data['summary']['report']

        # Date
        date = datetime.strptime(day['localDate'], '%Y-%m-%d')
        timestamp = int(date.strftime("%s")) * 1000
        name = 'Today'
        if is_first:
            is_first = False
            if is_night:
                name = 'Tonight'
        else:
            name = date.strftime('%A')

        # Weather Type
        type_id = day['weatherType']
        type_text = day['weatherTypeText']

        # Temperature
        temperature_high_c = day['maxTempC']
        temperature_high_f = day['maxTempF']
        temperature_low_c = day['minTempC']
        temperature_low_f = day['minTempF']

        # Wind
        wind_direction_code = day['windDirection']
        wind_direction_text = day['windDirectionFull']
        wind_speed_kph = day['windSpeedKph']
        wind_speed_mph = day['windSpeedMph']

        report = {
            'name': name,
            'date': timestamp,
            'type': {
                'id': type_id,
                'description': type_text
            },
            'temperature': {
                'high': { 'c': temperature_high_c, 'f': temperature_high_f },
                'low': { 'c': temperature_low_c, 'f': temperature_low_f }
            },
            'wind': {
                'direction': { 'code': wind_direction_code, 'description': wind_direction_text },
                'speed': { 'kph': wind_speed_kph, 'mph': wind_speed_mph }
            }
        }

        report['summary'] = format_summary(report)

        forecasts.append(report)

    return (location, forecasts)



def format_summary(report):
    weather = report['type']['description'].capitalize()
    high = report['temperature']['high']['c']
    low = report['temperature']['low']['c']
    format_string = '%s with a high of %d degrees and a low of %d degrees.'

    return format_string % (weather, high, low)

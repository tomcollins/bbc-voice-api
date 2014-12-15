import requests

location_endpoint = 'http://open.live.bbc.co.uk/locator/locations?s=%s&format=json&rs=1&place-types=settlement&order=importance'

def search_location(search):
    response = requests.get(location_endpoint % search)
    location_data = response.json()
    location_data = location_data['response']['locations']

    if len(location_data) == 0:
        return None

    location_data = location_data[0]

    return {
        'id': location_data['id'],
        'name': location_data['name'],
        'fullName': '%s, %s' % (location_data['name'], location_data['container']),
        'container': location_data['container'],
        'coordinates': {
            'latitude': location_data['latitude'],
            'longitude': location_data['longitude']
        }
    }

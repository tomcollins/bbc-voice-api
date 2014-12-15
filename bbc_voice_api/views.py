from pyramid.view import view_config

import content
import requests

@view_config(route_name='news', renderer='json')
def news(request):
    news_items = content.news.fetch_items()

    return {
        'list': news_items
    }

@view_config(route_name='weather', renderer='json')
def weather(request):
    location_id = request.params.get('location_id', '2653822')
    (location, forecast) = content.weather.fetch_forecasts(location_id)
    return {
        'location': location,
        'list': forecast
    }

@view_config(route_name='location', renderer='json')
def location(request):
    search = request.params.get('search', 'cardiff')
    location = content.location.search_location(search)
    return {
            'location': location
    }

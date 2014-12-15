from pyramid.view import view_config

import content
import requests

@view_config(route_name='news', renderer='json')
def news(request):
    topic_query = request.params.get('topic')
    topic = content.news.search_topics(topic_query, limit=1)

    topic_id = None
    if len(topic) > 0:
        topic = topic[0]
        topic_id = topic['id']

    news_items = content.news.fetch_items(topic_id)

    return {
        'topic': topic,
        'news': news_items
    }

@view_config(route_name='news-topics', renderer='json')
def topics(request):
    query = request.params.get('search')
    limit = request.params.get('limit', 20)

    results = content.news.search_topics(query, limit)

    return {
        'topics': results
    }

@view_config(route_name='weather', renderer='json')
def weather(request):
    location_id = request.params.get('location_id', '2653822')

    # Try to search for a location
    location = request.params.get('location')
    if location is not None:
        location = content.location.search_location(location)
        location_id = location['id']

    (location, forecast) = content.weather.fetch_forecasts(location_id)
    return {
        'location': location,
        'weather': forecast
    }

@view_config(route_name='location', renderer='json')
def location(request):
    search = request.params.get('search', 'cardiff')
    location = content.location.search_location(search)
    return {
            'location': location
    }

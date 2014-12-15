from pyramid.view import view_config

import requests

@view_config(route_name='news', renderer='json')
def language_parse(request):

    response = requests.get('http://newsapps-trevor-producer.cloud.bbc.co.uk/content/cps/news/front_page')

    items = []
    news_data = response.json()

    for article in news_data['relations']:
        if article['primaryType'] == 'bbc.mobile.news.item':
            content = article['content']
            items.append({
                'name': content['name'],
                'shortName': content['shortName'],
                'summary': content['summary'],
                'lastUpdated': content['lastUpdated']
            })

    return {
        'list': items
    }

from pyramid.view import view_config

import requests

@view_config(route_name='news', renderer='json')
def language_parse(request):

    response = requests.get('http://newsapps-trevor-producer.cloud.bbc.co.uk/content/cps/news/front_page')

    items = []
    news_data = response.json()

    # ipad-retina can be changed and styfull to thumbnail, styhalf
    # see https://confluence.dev.bbc.co.uk/display/newsapps/Moira+Image+Chef
    thumbnail_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/thumbnail'
    fullsize_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/styfull'

    for article in news_data['relations']:
        content = article['content']
        if content['format'] == 'bbc.mobile.news.format.textual':
            image_id = find_first_image(content['relations'])
            items.append({
                'name': content['name'],
                'shortName': content['shortName'],
                'summary': content['summary'],
                'lastUpdated': content['lastUpdated'],
                'images': {
                    'fullsize': fullsize_image_base_url + image_id,
                    'thumbnail': thumbnail_image_base_url + image_id
                }
            })

    return {
        'list': items
    }


def find_first_image(data):
    image_id = None
    for item in data:
        if item['primaryType'] == 'bbc.mobile.news.image':
            image_id = item['content']['id']
            break

    return image_id

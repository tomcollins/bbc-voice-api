import requests
import requests_cache
import os

import whoosh.index as whoosh_index
from whoosh.qparser import QueryParser


data_path = os.path.realpath(os.path.dirname(__file__) + '/../../data/')
requests_cache.install_cache(data_path + '/cache/voice_cache', expire_after=300)

content_endpoint = 'http://newsapps-trevor-producer.cloud.bbc.co.uk/content%s'

# ipad-retina can be changed and styfull to thumbnail, styhalf
# see https://confluence.dev.bbc.co.uk/display/newsapps/Moira+Image+Chef
thumbnail_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/thumbnail'
fullsize_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/styfull'

def fetch_items(topic_id = None):
    if topic_id is None:
        topic_id = '/cps/news/front_page'

    request_url = content_endpoint % topic_id

    print "Requesting: %s" % request_url

    response = requests.get(request_url)

    items = []

    if response.status_code != 200:
        print "Non 200: Got %s" % response.status_code
        return items

    news_data = response.json()

    index = 0
    limit = 20
    for article in news_data['relations']:
        content = article['content']
        if content['format'] == 'bbc.mobile.news.format.textual':
            relations = content['relations']
            image_id = find_first_image(relations)
            collection_name = find_collection_name(relations)

            item = {
                'name': content['name'],
                'shortName': content['shortName'],
                'summary': content['summary'],
                'lastUpdated': content['lastUpdated'],
                'collectionName': collection_name,
                'shareUrl': content['shareUrl']
            }

            if image_id is not None:
                item['images'] = {
                    'fullsize': fullsize_image_base_url + image_id,
                    'thumbnail': thumbnail_image_base_url + image_id
                }

            items.append(item)
            index = index + 1
            if index > limit:
                break

    return items


def search_topics(query, limit = 1):
    if query is None:
        return []

    current_path = os.path.dirname(__file__)
    ix = whoosh_index.open_dir(current_path + '/../../data/search/topics')
    qp = QueryParser('topic', schema=ix.schema)
    q = qp.parse(query)

    topics = []
    index = 0
    with ix.searcher() as searcher:
        results = searcher.search(q)
        for topic in results:
            the_topic = {
                'name': topic['topic'],
                'id': topic['id']
            }

            if 'description' in topic:
                the_topic['description'] = topic['description'],

            topics.append(the_topic)

            index = index + 1
            if index >= limit:
                break

    return topics


def find_first_image(data):
    """
    Finds the first image from a list of relations
    """
    image_id = None
    for item in data:
        if item['primaryType'] == 'bbc.mobile.news.image':
            image_id = item['content']['id']
            break

    return image_id


def find_collection_name(data):
    """
    Finds the collection name from relation
    """
    collection_name = None
    for item in data:
        if item['primaryType'] == 'bbc.mobile.news.collection':
            collection_name = item['content']['name']
            break

    return collection_name

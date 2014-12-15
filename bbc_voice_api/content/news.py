import requests

import whoosh.index as whoosh_index
from whoosh.qparser import QueryParser

def fetch_items():
    response = requests.get('http://newsapps-trevor-producer.cloud.bbc.co.uk/content/cps/news/front_page')

    items = []
    news_data = response.json()

    # ipad-retina can be changed and styfull to thumbnail, styhalf
    # see https://confluence.dev.bbc.co.uk/display/newsapps/Moira+Image+Chef
    thumbnail_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/thumbnail'
    fullsize_image_base_url = 'http://ichef.bbci.co.uk/moira/img/ipad-retina/v2/styfull'

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
                'collectionName': collection_name
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
    ix = whoosh_index.open_dir('data/search/topics')
    qp = QueryParser('topic', schema=ix.schema)
    q = qp.parse(query)

    topics = []
    index = 0
    with ix.searcher() as searcher:
        results = searcher.search(q)
        for topic in results:
            topics.append({
                'name': topic['topic'],
                #'description': topic['description'],
                'id': topic['id']
            })
            index = index + 1
            if index > limit:
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

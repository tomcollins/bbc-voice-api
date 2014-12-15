import requests

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

            items.append({
                'name': content['name'],
                'shortName': content['shortName'],
                'summary': content['summary'],
                'lastUpdated': content['lastUpdated'],
                'images': {
                    'fullsize': fullsize_image_base_url + image_id,
                    'thumbnail': thumbnail_image_base_url + image_id
                },
                'collectionName': collection_name
            })
            index = index + 1
            if index > limit:
                break

    return items


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

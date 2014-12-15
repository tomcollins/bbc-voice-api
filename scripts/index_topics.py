import json
from whoosh.index import create_in
from whoosh.fields import *


schema = Schema(
    topic=TEXT(stored=True),
    description=TEXT(stored=True),
    id=ID(stored=True)
)
ix = create_in('../data/search/topics', schema)
writer = ix.writer()

# Load the topics json
json_data=open('../data/content/topics.json').read()
data = json.loads(json_data)
topic_data = data['results']

for item in topic_data:
    topic_id = item['id']
    topic_name = item['name']
    topic_description = None
    if 'dis' in item:
        topic_description = item['dis']

    writer.add_document(
        topic = topic_name,
        description = topic_description,
        id = topic_id
    )

writer.commit()

import os
from mongo_utils import get_db_collection
from elasticsearch import AsyncElasticsearch

elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


async def connect_and_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = "http://localhost:9200"
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
        collections = await get_db_collection()
        for collection in collections:
            data_from_mongo = list(collection.find())
            for document in data_from_mongo:
                index_name = f"{collection.name}_index"
                await elasticsearch_client.index(index=index_name, body=document)

    except Exception as ex:
        print(f'Cant connect to elasticsearch: {ex}')


async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()


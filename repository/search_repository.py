import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from utils.mongo_utils import get_db_collection
from utils.elasticsearch_utils import get_elasticsearch_client
from models.models import User, Post, Comment


class SearchStudentRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: list[str]

    def __init__(self, indexs: list[str], elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = indexs

    async def create(self, user_id: str, user: User):
        await self._elasticsearch_client.create(index=self._elasticsearch_index[0], id=user_id, document=dict(user))

    async def update(self, user_id: str, user: User):
        await self._elasticsearch_client.update(index=self._elasticsearch_index[0], id=user_id, doc=dict(user))

    async def delete(self, user_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index[0], id=user_id)

    async def find_by_username(self, username: str):
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_index)

        if not index_exist:
            return []

        query = {
            "match": {
                "name": {
                    "query": username
                }
            }
        }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        users = list(map(lambda user: User(id=user['_id'], username=user['_source']['name'], email=user['_source']['email']), result))

        return users

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = await get_db_collection()

        return SearchStudentRepository(elasticsearch_index, elasticsearch_client)


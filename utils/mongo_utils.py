
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from models.models import User, Post, Comment

db_client: AsyncIOMotorClient = None


async def get_db_collection() -> list[AsyncIOMotorCollection]:
    mongo_db = "CoolTwitter"
    mongo_collections = ["users_collection","posts_collection", "comments_collection"]
    mc = []
    for collection in mongo_collections:
        mc.append(db_client.get_database(mongo_db).get_collection(collection))

    return mc


async def connect_and_init_mongo():
    global db_client
    mongo_uri = "mongodb://localhost:27017/"
    mongo_db = "CoolTwitter"
    mongo_collections = ["users_collection", "comments_collection", "posts_collection"]
    try:
        db_client = AsyncIOMotorClient(mongo_uri)
        await db_client.server_info()
        print(f'Connected to mongo with uri {mongo_uri}')
        if mongo_db not in await db_client.list_database_names():
            for collection_name in mongo_collections:
                await db_client.get_database(mongo_db).create_collection(collection_name)
            print(f'Database {mongo_db} created')

    except Exception as ex:
        print(f'Cant connect to mongo: {ex}')


def close_mongo_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


def map(obj: Any, collection: str) -> User | Post | Comment | None:
    if obj is None:
        return None
    if collection == 'users_collection':
        return User(id=str(obj['_id']), username=obj['username'], email=obj['email'], posts=obj['posts'], comments=obj['comments'])
    if collection == 'comments_collection':
        return Comment(id=str(obj['_id']), user_id=obj['user_id'], post_id=obj['post_id'], text=obj['text'])
    if collection == 'posts_collection':
        return Post(id=str(obj['_id']), user_id=obj['user_id'], title=obj['title'], content=obj['content'], comments=obj['comments'])
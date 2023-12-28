from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_db_collection, get_filter, map
from models.models import User, Post, Comment


class Repository:
    _db_collections: list[AsyncIOMotorCollection]

    def __init__(self, db_collections: list[AsyncIOMotorCollection]):
        self._db_collections = db_collections

    async def create(self, user: User) -> str: # создание юзера
        insert_result = await self._db_collections[0].insert_one(dict(user))
        return str(insert_result.inserted_id)
    

    async def get_all(self, collection: int) -> list[User] | list[Post] | list[Comment]: # вся коллекция
        db = []
        async for obj in self._db_collections[collection].find():
            db.append(map(obj))
        return db

    async def get_by_id(self, id: int, collection: int) -> User | Post | Comment | None:
        print(f'Get {id} from {collection}')
        obj = await self._db_collections[collection].find_one(get_filter(id))
        return map(obj)

    async def update(self, id: int, obj, collection: int) -> User | Post | Comment | None:
        updated_obj = await self._db_collections[collection].find_one_and_replace(get_filter(id), dict(obj))
        return map(updated_obj)
    ##########################################
    async def create_post(self, user: User, post: Post) -> str: # юзер создаёт пост
        

        insert_result = await self._db_collections[1].insert_one(dict(post))
        return str(insert_result.inserted_id)
    async def create_comment(self, user: User, post: Post, comment: Comment) -> str: # юзер создаёт пост

        insert_result = await self._db_collections[2].insert_one(dict(comment))
        return str(insert_result.inserted_id)
    ############################################


    async def delete(self, id: int, collection: int) -> User | Post | Comment | None:
        db_student = await self._db_collections[collection].find_one_and_delete(get_filter(id))
        return map(db_student)

    @staticmethod
    def get_instance(db_collections: AsyncIOMotorCollection = Depends(get_db_collection)):
        return Repository(db_collections)
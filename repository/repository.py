from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_db_collection, get_filter, map
from models.models import User, Post, Comment
from models.models import UserUpdate, PostUpdate, CommentUpdate

class Repository:
    _db_collections: list[AsyncIOMotorCollection]

    def __init__(self, db_collections: list[AsyncIOMotorCollection]):
        self._db_collections = db_collections

    async def create(self, user: UserUpdate) -> str: # создание юзера
        insert_result = await self._db_collections[0].insert_one(dict(user))
        return str(insert_result.inserted_id)

    async def get_all(self, collection: int) -> list[User] | list[Post] | list[Comment]: # вся коллекция
        db = []
        async for obj in self._db_collections[collection].find():
            db.append(map(obj, self._db_collections[collection].name))
        return db

    async def get_by_id(self, id: str, collection: int) -> User | Post | Comment | None:
        print(f'Get {id} from {collection}')
        obj = await self._db_collections[collection].find_one(get_filter(id))
        return map(obj, self._db_collections[collection].name)

    async def update(self, id: str, obj, collection: int) -> User | Post | Comment | None:
        updated_obj = await self._db_collections[collection].find_one_and_replace(get_filter(id), dict(obj))
        return map(updated_obj)
    ########################################nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    async def create_post(self, post: PostUpdate) -> str: # юзер создаёт пост
        user = map(await self._db_collections[0].find_one(get_filter(post.user_id)), self._db_collections[0].name)
        if (user.posts != None):
            user.posts.append(post.id)
        else:
            user.posts = [post.id]
        updated_obj = await self._db_collections[0].find_one_and_replace(get_filter(post.user_id), dict(user))
        insert_result = await self._db_collections[1].insert_one(dict(post))
        return str(insert_result.inserted_id)
    
    async def create_comment(self, comment: CommentUpdate) -> str: # юзер создаёт пост
        user = map(await self._db_collections[0].find_one(get_filter(comment.user_id)), self._db_collections[0].name)
        post = map(await self._db_collections[1].find_one(get_filter(comment.post_id)), self._db_collections[1].name)

        if (user.comments != None):
            user.comments.append(comment.id)
        else:
            user.comments = [comment.id]

        if (post.comments != None):
            post.comments.append(comment.id)
        else:
            post.comments = [comment.id]

        updated_obj1 = await self._db_collections[0].find_one_and_replace(get_filter(comment.user_id), dict(user))
        updated_obj2 = await self._db_collections[1].find_one_and_replace(get_filter(comment.post_id), dict(post))

        insert_result = await self._db_collections[2].insert_one(dict(comment))
        return str(insert_result.inserted_id)
    ############################################


    async def delete(self, id: int, collection: int) -> User | Post | Comment | None:
        db_student = await self._db_collections[collection].find_one_and_delete(get_filter(id))
        return map(db_student)

    @staticmethod
    async def get_instance():
        db_coll = await get_db_collection()
        r = Repository(db_coll)
        #print(f"==={type(db_coll)}")
        return r
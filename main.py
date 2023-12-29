import string

import pymongo
import random
from bson import ObjectId
import asyncio
from fastapi import FastAPI
# from bson import ObjectId
from models.models import User, Comment, Post
from utils.mongo_utils import connect_and_init_mongo
from repository.repository import Repository
from models.models import UserUpdate, PostUpdate, CommentUpdate
class MongoDB:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.my_database = self.client["CoolTwitter"]
        self.users_collection = self.my_database["users_collection"]
        self.posts_collection = self.my_database["posts_collection"]
        self.comments_collection = self.my_database["comments_collection"]

    def insert_to_collection(self, obj):
        collection_name = obj.collection
        collection = self.my_database[collection_name]
        new_dict = obj.__dict__
        inserted_id = collection.insert_one(new_dict).inserted_id

        print(f"объект вставлен в коллекцию с названием : {collection_name} с ID: {inserted_id}")

    def delete_from_collection(self, obj):
        collection_name = obj.collection
        collection = self.my_database[collection_name]

        result = collection.delete_one({'id': obj.id})

        if result.deleted_count == 1:
            print(f"Объект удален из коллекции : {collection_name}")
        else:
            print(f"Объект не найден в коллекции : {collection_name}")

    def find_in_collection(self, _id, collection_name):
        collection = self.my_database[collection_name]

        print(collection.find_one({'id': _id}))
        return collection.find_one({'id': _id})

    def update_elem_in_collection(self, obj, field_to_change, change):
        collections_name = obj.collection
        collection = self.my_database[collections_name]

        collection.update_one({'id': obj.id}, {'$set': {field_to_change: change}})
from handler.event_handlers import startup, shutdown
from router.router import router



app = FastAPI()
app.include_router(router, tags=["User", "Post", "Comment"], prefix="/api/app")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)




    
    #await r.delete_comment(id=comm1)
    
    #
    #user_id2 = await r.create(UserUpdate(username="User1", email="email2@mail.com"))
    #user_id3 = await r.create(UserUpdate(username="User3", email="email3@mail.com"))

    #
    #post2 = await r.create_post(PostUpdate(user_id=user_id2, title='What are we doing2', content=["lol2"]))
    #post3 = await r.create_post(PostUpdate(user_id=user_id3, title='What are we doing3', content=["lol3"]))

    

    # u = await r.get_by_id(id=2, collection=0)
    # print(u)
    # us = await r.get_all(collection=0)
    #print(us)
    # p = Post(id=1, user_id=1, title="Don't do crimes", content=["crimes are bad"])
    #await r.create_post(post=p)
    # c = Comment(id = 0, user_id=1, post_id=0, text="no, crimes are bad!")
    # await r.create_comment(c)
    #await r.create(User(id=1, username="User1", email="email@mail.com"))
    #print(f"---{r._db_collections}")
    # print (generate_users())
    # db = MongoDB()
    # # db.delete_from_collection(user1)
    # db.find_in_collection(2, 'users_collection')
    # db.update_elem_in_collection(user2, 'username', 'New_username')
    # db.find_in_collection(2, 'users_collection')


'''
r = await  Repository.get_instance()
    user_id1 = await r.create(UserUpdate(username="User1", email="email1@mail.com"))
    user_id2 = await r.create(UserUpdate(username="User2", email="email2@mail.com"))
    user_id3 = await r.create(UserUpdate(username="User3", email="email3@mail.com"))
    post1 = await r.create_post(PostUpdate(user_id=user_id1, title='What are we doing1', content=["lol1"]))
    post2 = await r.create_post(PostUpdate(user_id=user_id2, title='What are we doing2', content=["lol2"]))

    comm1 = await r.create_comment(CommentUpdate(user_id=user_id1, post_id=post1, text="oooo2131ooooo"))
    comm2 = await r.create_comment(CommentUpdate(user_id=user_id3, post_id=post2, text="ooo2312oooooo"))
    await r.delete_post(id=post1)
    await r.delete_comment(id=comm2)
'''

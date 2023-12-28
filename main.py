import string

import pymongo
import random
from bson import ObjectId
import asyncio
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


def generate_comments(user_id, post_id):
    num_comments = random.randint(1, 5)
    comments = []
    for i in range(num_comments):
        text = ''.join(random.choices(string.ascii_letters + string.digits + string.whitespace, k=50))
        comment_id = user_id * 1000 + post_id * 100 + i * 10 + random.randint(100, 2000)
        comment = Comment(id=comment_id, user_id=user_id, post_id=post_id, text=text)
        attrs = vars(comment)
        print(attrs)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        comments.append(comment)

    return comments


def generate_posts(user_id):
    num_posts = random.randint(1, 5)
    posts = []
    for i in range(num_posts):
        title = ''.join(random.choices(string.ascii_letters + string.digits + string.whitespace, k=30))
        content = ''.join(random.choices(string.ascii_letters + string.digits + string.whitespace, k=10))
        post_id = user_id + i + random.randint(100, 2000)

        comment_ids = [comment.id for comment in generate_comments(user_id, post_id)]
        content_list = [content]
        post = Post(id=post_id, user_id=user_id, title=title, content=content_list, comments=comment_ids)
        attrs = vars(post)
        print(attrs)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        posts.append(post)

    return posts


def generate_users():
    domains = ['yandex.ru', 'mail.yandex.com', 'outlook.com', 'mai.com']
    users = []

    for i in range(1, 6):  # Generating 10 objects
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        domain = random.choice(domains)
        email = ''.join(random.choices(string.ascii_lowercase, k=7)) + f"@{domain}"

        post_ids = [post.id for post in generate_posts(i)]
        user = User(id=i, username=username, email=email, posts=post_ids)
        attrs = vars(user)
        print(attrs)
        # print(', '.join("%s: %s" % item for item in attrs.items()))
        users.append(user)

    return users


async def main():
    
    await connect_and_init_mongo()
    r = await  Repository.get_instance()
    # await r.create(UserUpdate(username="User3", email="email2@mail.com"))
    user = await r.get_by_id(id=ObjectId('658dccf4dbfb770547c7d9d8'), collection=0)
    await r.create_post(PostUpdate(user_id=user.id, title='What are we doing', content=["lol"]))
    
    print(user)
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


if __name__ == "__main__":
    asyncio.run(main())
    



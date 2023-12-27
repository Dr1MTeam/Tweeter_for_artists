import string

import pymongo
import random
# from bson import ObjectId
# from models import User, Comment, Post


class User:
    def __init__(self, _id, username, email):
        self.id = _id
        self.collection = 'users_collection'
        self.username = username
        self.email = email
        self.posts = []


class Comments:
    def __init__(self, _id, text, user_id, post_id):
        self.id = _id
        self.user_id = user_id
        self.post_id = post_id
        self.collection = 'comments_collection'
        self.text = text


class Posts:
    def __init__(self, _id, title, content, user_id):
        self.id = _id
        self.user_id = user_id
        self.collection = 'posts_collection'
        self.title = title
        self.content = content
        self.comments = []


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


def generate_users():
    domains = ['yandex.ru', 'mail.yandex.com', 'outlook.com', 'mai.com']
    users = []

    for i in range(1, 6):  # Generating 10 objects
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        domain = random.choice(domains)
        email = ''.join(random.choices(string.ascii_lowercase, k=7)) + f"@{domain}"

        users.append(User(_id=i, username=username, email=email))

    return users

def main():

    user1 = User(1, "username1", "email@user1")

    post1 = Posts(1, 'fkgdjg', 'fkgjdfg', 1)

    user2 = User(2, "username2", "email@user2")
    user3 = User(3, "username3", "email@user3")
    db = MongoDB()
    # db.delete_from_collection(user1)
    db.find_in_collection(2, 'users_collection')
    db.update_elem_in_collection(user2, 'username', 'New_username')
    db.find_in_collection(2, 'users_collection')


if __name__ == "__main__":
    main()


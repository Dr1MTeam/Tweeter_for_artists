from typing import Mapping, Any

import pymongo
from bson import ObjectId
from pydantic import BaseModel
from pymongo.database import Database
from models import User, Comment, Post


class UserData:
    def init(self, username, email):
        self.username = username
        self.email = email
        self.posts = []


def connect_to_mongo():
    # Подключение к MongoDB (по умолчанию к localhost:27017)
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Создание базы данных
    mydatabase = client["mydatabase"]

    # Создание коллекции
    mycollection = mydatabase["mycollection"]

    # Создание пользователя
    user1 = User(id=2, username="user2", email="user2@example.com")

    # Вставка пользователя в коллекцию
    user_id = mycollection.insert_one(user1.model_dump()).inserted_id
    post = {"title": "New Post Title", "content": "New Post Content"}
    update_query = {"$push": {"posts": post}}

    mycollection.update_one({"_id": ObjectId(user_id)}, update_query)


    # Пример добавления нового поста
def main():
    connect_to_mongo()

    user1 = User(id=0, username="user1", email="user1@example.com")
    user2 = User(id=1, username="user2", email="user2@example.com")

    post1 = Post(id=0, title="Title 1", content="Content 1")
    post2 = Post(id=0, title="Title 2", content="Content 2",)

    comment1 = Comment(id=0, text="Comment 1")
    comment2 = Comment(id=1, text="Comment 2")


if __name__ =="__main__":
    main()


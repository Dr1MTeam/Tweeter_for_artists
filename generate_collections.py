from faker import Faker
from typing import List, Optional
from pymongo import MongoClient
from pydantic import BaseModel

fake = Faker()

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Создание или подключение к базе данных "mydatabase"
db = client['mydatabase']

# Создание коллекции пользователей
user_collection = db['user_collection']


class User(BaseModel):
    id: str
    username: str
    email: str
    posts: Optional[List[int]] = None
    comments: Optional[List[int]] = None


def generate_fake_user():
    user_id = fake.uuid4()
    return User(
        id=user_id,
        username=fake.user_name(),
        email=fake.email(),
        posts=[fake.random_int(min=1, max=1000) for _ in range(fake.random_int(min=0, max=5))],
        # Fake posts here after generating
        comments=[fake.random_int(min=1, max=1000) for _ in range(fake.random_int(min=0, max=5))]
        # Fake comments here after generating
    )


def insert_users_into_collection(collection, num_users):
    users = [generate_fake_user() for _ in range(num_users)]
    collection.insert_many([user.model_dump() for user in users])


# Пример использования:
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']

user_collection = db['user_collection']

# Добавление пользователей в коллекцию пользователей
insert_users_into_collection(user_collection, num_users=10)

# Получение всех пользователей
all_users = user_collection.find()

# Вывод данных
for user in all_users:
    print(user)

"""
# Создание коллекции постов
post_collection = db['post_collection']

# Создание коллекции комментариев
comment_collection = db['comment_collection']

class User:
    def init(self, _id, username, email, posts):
        self.id = _id
        self.collection = 'user_collection'
        self.username = username
        self.email = email
        self.posts = posts


class Comment:
    def init(self, _id, text, user_id, post_id):
        self.id = _id
        self.user_id = user_id
        self.post_id = post_id
        self.collection = 'comments_collection'
        self.text = text

class Post:
    def init(self, _id, user_id,title, content, comments):
        self.id = _id
        self.user_id = user_id
        self.collection = 'posts_collection'
        self.title = title
        self.content = content
        self.comments = comments



class Comment:

    id: int
    text: str

class Post(BaseModel):
    id: int
    title: str
    content: str
    comments: List[Comment] = []

class User(BaseModel):
    id: int
    username: str
    email: str
    posts: List[Post] = []

def generate_users(num_users):
    users = []
    for i in range(num_users):
        user_id = fake.random_int(min=1, max=1000)
        user = User(id=user_id, username=fake.user_name(), email=fake.email(), posts=[])
        users.append(user)
    return users



def generate_posts():
    posts = []
    domains = ['yandex.ru', 'mail.yandex.com', 'outlook.com', 'mai.com']
    for i in range(num_posts):
        post_id = fake.random_int(min=1, max=1000)
        post = Post(id=post_id, title=fake.sentence(), content=fake.paragraph(), comments=[],)
        posts.append(post)
    return posts

def generate_comments(post_id, num_comments):
    comments = []
    for i in range(num_comments):
        comment_id = fake.random_int(min=1, max=1000)
        comment = Comment(id=comment_id, text=fake.text())
        comments.append(comment)
    return comments

def insert_into_collection(collection, data):
    collection.insert_many([item.model_dump() for item in data])

# Пример использования:
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']

user_collection = db['user_collection']
post_collection = db['post_collection']
comment_collection = db['comment_collection']

# Генерация и вставка пользователей
num_users = 10
users = generate_users(num_users)
insert_into_collection(user_collection, users)

# Генерация и вставка постов и комментариев
for user in users:
    num_posts = fake.random_int(min=1, max=5)
    posts = generate_posts(user.id, num_posts)
    user.posts.extend(posts)
    insert_into_collection(post_collection, posts)

    for post in posts:
        num_comments = fake.random_int(min=0, max=10)
        comments = generate_comments(post.id, num_comments)
        post.comments.extend(comments)
        insert_into_collection(comment_collection, comments)"""

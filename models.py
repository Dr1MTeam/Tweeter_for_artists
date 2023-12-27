from pydantic import BaseModel
from typing import List


class Comment(BaseModel):
    id: int
    text: str


class Post(BaseModel):
    id: int          # == userid == author id
    # post_collection: str
    title: str
    content: str
    comments: List[int]


class User(BaseModel):
    id: int
    # user_collection: str
    username: str
    email: str
    posts: List[int]


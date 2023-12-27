from pydantic import BaseModel
from typing import List


class Comment(BaseModel):
    id: int
    text: str


class Post(BaseModel):
    id: int          # == userid == author id
    title: str
    content: str
    comments: List[Comment] = []


class User(BaseModel):
    id: int
    username: str
    email: str
    posts: List[Post] = []
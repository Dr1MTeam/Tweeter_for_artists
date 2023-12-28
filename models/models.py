from pydantic import BaseModel
from typing import List, Optional, Union


class User(BaseModel):
    id: int
    collection: str = 'users_collection'
    username: str
    email: str
    posts: Optional[List[int]] = None
    comments: Optional[List[int]] = None



class Comment(BaseModel):
    id: int
    user_id: int
    post_id: int
    collection: str = 'comments_collection'
    text: str


class Post(BaseModel):
    id: int
    user_id: int
    collection: str = 'posts_collection'
    title: str
    content: List[Union[str, bytes]]
    comments: Optional[List[int]] = None


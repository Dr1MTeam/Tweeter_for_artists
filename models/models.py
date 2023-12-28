from pydantic import BaseModel
from typing import List, Optional, Union


class User(BaseModel):
    id: int
    username: str
    email: str
    posts: Optional[List[int]] = None
    comments: Optional[List[int]] = None


class Comment(BaseModel):
    id: int
    user_id: int
    post_id: int
    text: str


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: List[Union[str, bytes]]
    comments: Optional[List[int]] = None


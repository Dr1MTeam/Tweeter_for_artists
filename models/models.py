from pydantic import BaseModel
from typing import List, Optional, Union


class User(BaseModel):
    id: str
    username: str
    email: str
    posts: Optional[List[int]] = None
    comments: Optional[List[int]] = None

class UserUpdate(BaseModel):
    username: str
    email: str
    posts: Optional[List[int]] = None
    comments: Optional[List[int]] = None

class Comment(BaseModel):
    id: str
    user_id: str
    post_id: str
    text: str

class CommentUpdate(BaseModel):
    user_id: str
    post_id: str
    text: str

class Post(BaseModel):
    id: str
    user_id: str
    title: str
    content: List[Union[str, bytes]]
    comments: Optional[List[int]] = None

class PostUpdate(BaseModel):
    user_id: str
    title: str
    content: List[Union[str, bytes]]
    comments: Optional[List[int]] = None



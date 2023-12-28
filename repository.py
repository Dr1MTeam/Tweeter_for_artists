from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from utils.mongo_utils import get_db_collection, get_filter, map_student
from models.models import User, Post, Comment

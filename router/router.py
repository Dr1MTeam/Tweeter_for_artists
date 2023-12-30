from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from pymemcache import HashClient
from starlette.responses import Response

from cache.memcached_utils import get_memcached_client
from repository.repository import Repository
from repository.search_repository import SearchStudentRepository
from models.models import User, Post, Comment
from models.models import UserUpdate, PostUpdate, CommentUpdate

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}




@router.get("/user/all", tags=["User"])
async def get_all(repository: Repository = Depends(Repository.get_instance)) -> list[User] | list[Post] | list[Comment]:
    return await repository.get_all(0)
@router.get("/post/all", tags=["Post"])
async def get_all(repository: Repository = Depends(Repository.get_instance)) -> list[User] | list[Post] | list[Comment]:
    return await repository.get_all(1)
@router.get("/comment/all", tags=["Comment"])
async def get_all(repository: Repository = Depends(Repository.get_instance)) -> list[User] | list[Post] | list[Comment]:
    return await repository.get_all(2)

@router.get("/debug_get/{collection}/{user_id}")
async def get(collection: int, user_id: str, repository: Repository = Depends(Repository.get_instance),
                                             memcached_client: HashClient = Depends(get_memcached_client)) -> User | Post | Comment:
    
    obj = await repository.get_by_id(id = user_id, collection = collection)
    return obj

@router.get("/user/filter", tags=["User"])
async def get_by_name(username: str, repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    return await repository.find_by_username(username = username)


@router.get("/user/{user_id}", response_model=User, tags=["User"])
async def get_by_id(user_id: str,
                    repository: Repository = Depends(Repository.get_instance),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user = memcached_client.get(str(user_id))
    if user is not None:
        return user

    user = await repository.get_by_id(str(user_id), collection=0)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    memcached_client.add(user_id, user)
    return user


@router.post("/user/", tags=["User"])
async def add_user(user: UserUpdate,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    id = await repository.create(user)
    await search_repository.create(id, user)
    return id
@router.post("/post/", tags=["Post"])
async def add_post(post: PostUpdate,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    id = await repository.create_post(post)
    await search_repository.create_post(id, post)
    return id
@router.post("/comment/", tags=["Comment"])
async def add_comment(comment: CommentUpdate,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    id = await repository.create_comment(comment)
    # await search_repository.create_(id, comment)
    return id



@router.delete("/user/{user_id}")
async def remove_user(user_id: str,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await repository.delete_user(user_id)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete(user_id)
    return Response()

@router.delete("/post/{post_id}")
async def remove_post(post_id: str,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(post_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    post = await repository.delete_post(post_id)
    if post is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete_post(post_id)
    return Response()

@router.delete("/comment/{post_id}")
async def remove_comment(comment_id: str,
                         repository: Repository = Depends(Repository.get_instance)) -> Response:
    if not ObjectId.is_valid(comment_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    comment = await repository.delete_post(comment_id)
    return Response()


@router.put("/user/{user_id}", response_model=User)
async def update_user(user_id: str,
                         user_model: UserUpdate,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    user = await repository.update(user_id, user_model)
    if user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(user_id, user_model)
    return user

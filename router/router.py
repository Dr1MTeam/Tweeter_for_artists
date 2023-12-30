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

@router.get("/collection/{collection}/{user_id}")
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

'''

@router.delete("/{student_id}")
async def remove_user(user_id: int,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.delete(student_id)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete(student_id)
    return Response()


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: str,
                         student_model: UpdateStudentModel,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.update(student_id, student_model)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(student_id, student_model)
    return student

'''
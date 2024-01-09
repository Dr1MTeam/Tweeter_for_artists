import os
import random
import uuid

import requests

from dotenv import load_dotenv
load_dotenv('tests/tests.env')


API_URL=os.getenv('API_URL')


def create_user(username=None, email=None):
    if username is None:
        username = str(uuid.uuid4())
    if email is None:
        email = str(uuid.uuid4())
    user_url = f'{API_URL}/user/'
    response = requests.post(user_url, json={
                                                "username": username,
                                                "email": email,
                                                "posts": None,
                                                "comments": None
})
    return response

def create_post(user_id, title=None, content=None):
    if title is None:
        title = str(uuid.uuid4())
    if content is None:
        content = [str(uuid.uuid4())]
    post_url = f'{API_URL}/post/'
    response = requests.post(post_url, json={
                                            "user_id": user_id,
                                            "title": title,
                                            "content": content,
                                            "comments": None
})
    return response


def test_user_creation():
    username = str(uuid.uuid4())
    email = str(uuid.uuid4())
    user_url = f'{API_URL}/user/'
    created_user_id = create_user(username=username, email=email)
    cleaned_user_id = created_user_id.text.strip('"')
    user_url = f'{API_URL}/user/{cleaned_user_id}'
    user = requests.get(user_url).json()
    assert user['username'] == username
    assert user['email'] == email
    requests.delete(f'{API_URL}/user/{cleaned_user_id}')

def test_search_user_by_name():
    username = str(uuid.uuid4())
    email = str(uuid.uuid4())
    created_ids = [create_user(username, email).text.strip('"'), create_user().text.strip('"'), create_user().text.strip('"')]
    # print(created_ids)
    users = requests.get(f'{API_URL}/user/filter?username={username}').json()
    assert len(users) == 1
    assert users[0]['username'] == username
    assert users[0]['email'] == email
    for created_id in created_ids:
        requests.delete(f'{API_URL}/user/{created_id}')
def test_post_creation():
    
    created_user_id = create_user()
    cleaned_user_id = created_user_id.text.strip('"')
    user_url = f'{API_URL}/user/{cleaned_user_id}'

    title = str(uuid.uuid4())
    content = [str(uuid.uuid4())]
    created_post_id = create_post(user_id=cleaned_user_id, title=title, content=content)
    cleaned_post_id = created_post_id.text.strip('"')
    post_url = f'{API_URL}/post/{cleaned_post_id}'
    post = requests.get(post_url).json()
    print(post)
    print(cleaned_user_id)
    
    requests.delete(user_url)
    requests.delete(post_url)


test_post_creation()


    

# post = requests.get(f'{API_URL}/post/filter?title={title}').json()
# create_post(user_id='658ee6f203af1c5ef8f1db64')
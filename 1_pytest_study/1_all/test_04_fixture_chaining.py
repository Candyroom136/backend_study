import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def database():
    return {"users": [], "posts": []}

@pytest_asyncio.fixture
async def user(database):
    user_data = {"id": 1, "name": "김철수"}
    database["users"].append(user_data)
    return user_data

@pytest_asyncio.fixture
async def post(database, user):
    post_data = {"id": 1, "title": "첫 게시글", "author_id": user["id"]}
    database["posts"].append(post_data)
    return database

@pytest.mark.asyncio
async def test_user_post_relationship(database, user):
    assert len(database["users"]) == 1
    assert len(database["posts"]) == 1
    assert database["posts"][0]["author_id"] == user["id"]
    assert database["posts"][0]["title"] == post["title"]
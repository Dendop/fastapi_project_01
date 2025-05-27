import pytest
from app import schema

def test_get_all_posts(authorized_client,test_posts):
    # print(f"Test posts created {test_posts}")
    res = authorized_client.get("/posts")
    #print(f"Response JSON: {res.json()}")
    # print(f"Response status code: {res.status_code}")
    
    assert res.status_code == 200
    assert len(res.json()) == 3       #len(test_posts) -> we had 3 but adding test_user2 now we have 4 and we query 3 posts by "id"

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_not_existing_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/99999")
    
    assert res.status_code == 404
    
@pytest.mark.parametrize("title, content",[
    ("my day", "it was good just my back hurts"),
    ("Tuesday", "the sausages were awesome")
])  
def test_create_post(authorized_client, test_user,test_user2, test_posts, title, content):
    res = authorized_client.post("/posts", json={"title": title, "content": content})
    created_post = schema.ResponsePost(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == test_user["id"]
    # print(f"Checking res : {res}")
    # print(f"Checking newly created post: {created_post}")
    # print(f"THIS IS USER : {type(test_user)}")
    
def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 200
    
def test_delete_other_user_post(authorized_client,test_user,test_posts): #need to use test_user2
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "in cage",
        "content": "I been held as prisoner for Starks",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_posts = schema.ResponsePost(**res.json())
    assert res.status_code == 200
    assert updated_posts.id == data["id"]
    assert updated_posts.title == data["title"]
    
def test_update_another_users_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Up in Tower",
        "content": "I have seen it all and they tossed me down the tower",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
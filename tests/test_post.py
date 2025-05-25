def test_get_all_posts(authorized_client,test_posts):
    # print(f"Test posts created {test_posts}")
    res = authorized_client.get("/posts")
    # print(f"Response JSON: {res.json()}")
    # print(f"Response status code: {res.status_code}")
    
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_not_existing_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/99999")
    
    assert res.status_code == 404
def test_get_all_posts(authorized_client,test_posts):
    print(f"Test posts created {test_posts}")
    res = authorized_client.get("/posts")
    print(f"Response JSON: {res.json()}")
    print(f"Response status code: {res.status_code}")
    
    assert res.status_code == 200
    #assert len(res.json()) == len(test_posts)

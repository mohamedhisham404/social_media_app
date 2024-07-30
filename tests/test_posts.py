def test_get_all_posts(authorized_client, test_posts):
    reponse = authorized_client.get("/posts/")
    print(reponse.json)
    assert reponse.status_code == 200
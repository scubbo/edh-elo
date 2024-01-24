# These tests expect that the database starts empty.
# TODO: create tests with initialized states


def test_add_and_retrieve(client):
    response = client.get("/player/1", headers={"Content-Type": "application/json"})
    assert response.status_code == 404

    client.post(
        "/player", headers={"Content-Type": "application/json"}, json={"name": "jason"}
    )
    response_1 = client.get("/player/1", headers={"Content-Type": "application/json"})
    assert response_1.json["name"] == "jason"

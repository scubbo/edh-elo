from typing import Mapping

import httpx
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_add_and_retrieve_player(test_client: TestClient):
    response = _json_get(test_client, "/player/1")
    assert response.status_code == 404

    create_player_response = _json_post(client, "/player", {"name": "jason"})
    assert create_player_response.status_code == 201

    response_1 = _json_get(client, "/player/1")
    assert response_1.json()["name"] == "jason"

    # Cleanup
    # TODO - put this in a finally clause (or similar as provided by pytest)
    delete_response = _json_delete(client, "/player/1")
    assert delete_response.status_code == 204


def test_add_and_retrieve_deck(test_client: TestClient):
    not_found_response = _json_get(test_client, "/deck/1")
    assert not_found_response.status_code == 404

    # Try (and fail) to create a deck owned by a non-existent player
    invalid_owner_response = _json_post(
        test_client, "/deck", {"name": "Baby's First Deck", "owner_id": 1}
    )
    assert invalid_owner_response.status_code == 400
    assert invalid_owner_response.json()['detail'] == "Owner id 1 not found"

    create_jim_response = _json_post(test_client, "/player", {"name": "jim"})
    assert create_jim_response.status_code == 201
    jim_id = create_jim_response.json()["id"]

    create_deck_response = _json_post(
        test_client, "/deck", {"name": "Baby's First Deck", "owner_id": str(jim_id)}
    )
    assert create_deck_response.status_code == 201
    # _Should_ always be 1, since we expect to start with an empty database, but why risk it?
    deck_id = create_deck_response.json()["id"]

    get_deck_response = _json_get(test_client, f"/deck/{deck_id}")
    assert get_deck_response.status_code == 200
    assert get_deck_response.json()["name"] == "Baby's First Deck"

    # Very basic HTML testing
    html_response = test_client.get(f"/deck/{deck_id}")
    assert "owned by jim" in html_response.text

    # Cleanup
    delete_response = _json_delete(test_client, f"/deck/{deck_id}")
    assert delete_response.status_code == 204


def _json_get(c: TestClient, path: str) -> httpx.Response:
    return c.get(f'/api{path}', headers={"Content-Type": "application/json"})


def _json_post(c: TestClient, path: str, body: Mapping) -> httpx.Response:
    return c.post(f'/api{path}', headers={"Content-Type": "application/json"}, json=body)


def _json_delete(c: TestClient, path: str) -> httpx.Response:
    return c.delete(f'/api{path}', headers={"Content-Type": "application/json"})

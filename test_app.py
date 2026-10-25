from app import app, plants
import pytest


@pytest.fixture
def client():
    app.config["TESTING"] = True
    plants.clear()
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "ok"


def test_add_plant_calculates_schedule(client):
    payload = {
        "name": "Fern",
        "species": "Boston",
        "frequency": "5",
        "last_watered": "2026-09-01",
    }
    post_res = client.post("/add", data=payload, follow_redirects=True)
    assert post_res.status_code == 200
    assert b"Fern" in post_res.data
    assert b"2026-09-06" in post_res.data

    api_res = client.get("/api/plants")
    assert len(api_res.json) == 1
    assert api_res.json[0]["next_due"] == "2026-09-06"


def test_invalid_input_rejected(client):
    bad_payload = {
        "name": "",
        "species": "Cactus",
        "frequency": "-3",
        "last_watered": "2026-09-01",
    }
    res = client.post("/add", data=bad_payload)
    assert res.status_code == 400

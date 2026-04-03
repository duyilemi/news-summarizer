import pytest
import json
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_summaries_no_data(monkeypatch):
    # Mock glob.glob directly
    monkeypatch.setattr('glob.glob', lambda pattern: [])
    response = client.get("/summaries")
    assert response.status_code == 404
    assert "No summaries found" in response.json()["detail"]


def test_get_summaries_with_data(monkeypatch, tmp_path):
    import json
    dummy_data = [{"title": "Test", "summary": "Test summary", "url": "http://test.com", "published_at": "2024-01-01"}]
    dummy_file = tmp_path / "summaries_test.json"
    with open(dummy_file, "w") as f:
        json.dump(dummy_data, f)


    # Mock glob.glob to return this file
    monkeypatch.setattr('glob.glob', lambda pattern: [str(dummy_file)])
    # Mock os.path.getctime to return a fixed value (oldest file first, but we only have one)
    monkeypatch.setattr('os.path.getctime', lambda f: 0)
    response = client.get("/summaries")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test"
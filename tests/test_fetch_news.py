import pytest
from unittest.mock import patch, MagicMock
from src.fetch_news import fetch_top_headlines, save_raw_data
import json

@patch('src.fetch_news.requests.get')
def test_fetch_top_headlines_success(mock_get):
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "ok",
        "articles": [{"title": "Test", "description": "Test description"}]
    }
    mock_get.return_value = mock_response

    result = fetch_top_headlines(country="us", page_size=1)
    assert result["status"] == "ok"
    assert len(result["articles"]) == 1

@patch('src.fetch_news.requests.get')
def test_fetch_top_headlines_failure(mock_get):
    mock_get.side_effect = Exception("API error")
    with pytest.raises(Exception):
        fetch_top_headlines()

def test_save_raw_data(tmp_path):
    # tmp_path is a pytest fixture for temporary directory
    data = {"test": "data"}
    filepath = save_raw_data(data, filename="test.json")
    assert filepath.endswith("test.json")
    with open(filepath, "r") as f:
        saved = json.load(f)
    assert saved == data
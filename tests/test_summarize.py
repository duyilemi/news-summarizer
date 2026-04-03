import pytest
from unittest.mock import patch, MagicMock
from src.summarize import summarize_article, process_articles
import json

@patch('src.summarize.client')
def test_summarize_article(mock_client):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a summary."
    mock_client.chat.completions.create.return_value = mock_response

    result = summarize_article("Long article text here")
    assert result == "This is a summary."

def test_process_articles(tmp_path):
    raw_data = {
        "articles": [
            {"title": "Title1", "description": "This is a long enough description for testing purposes that exceeds the fifty character limit.", "url": "http://a.com", "publishedAt": "2024-01-01"},
            {"title": "Title2", "description": "Another sufficiently long description that will not be filtered out by the length check.", "url": "http://b.com", "publishedAt": "2024-01-02"}
        ]
    }
    raw_file = tmp_path / "raw.json"
    with open(raw_file, "w") as f:
        json.dump(raw_data, f)

    with patch('src.summarize.summarize_article', return_value="Mock summary"):
        output_path = process_articles(str(raw_file), output_filepath=str(tmp_path / "processed.json"))
        with open(output_path, "r") as f:
            summaries = json.load(f)
        assert len(summaries) == 2
from fastapi.testclient import TestClient
from api.api import app
from unittest.mock import patch

client = TestClient(app)


def test_chat_endpoint():
    payload = {
        "character_file": "data/characters/astra.yaml",
        "enable_user_memory": True,
        "user_name": "Jordan",
        "user_interests": "space exploration and adventure",
        "message": "Where are you now?",
        "model": "gpt-5-nano",
    }

    mock_response = {
        "response": "I'm currently aboard the Stellar Voyager, navigating through the Andromeda sector.",
        "status": 200,
    }

    with patch(
        "src.services.openai_service.OpenAIService.generate_response",
        return_value=mock_response,
    ):
        response = client.post("/chat", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data or "error" in data
        assert "status" in data
        if "response" in data:
            assert data["response"] == mock_response["response"]

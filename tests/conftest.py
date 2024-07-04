from unittest.mock import MagicMock

from openai.openai_object import OpenAIObject
import pytest



@pytest.fixture(autouse=True)
def set_env(monkeypatch, mocker):
    monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')
    monkeypatch.setenv('PROXY', 'test-proxy')
    mocker.patch('dotenv.load_dotenv', return_value=None)


@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch('openai_agent.repositories.dotenv.init', return_value=None)
    
    async def mock_openai_create(*args, **kwargs):
        print("Mock OpenAI create called")
        mock_message = MagicMock()
        mock_message.message = OpenAIObject()
        mock_message.message.role = 'assistent'
        mock_message.message.content = 'Response from OpenAI'
        response = MagicMock()
        response.choices = [mock_message]
        return response

    mocker.patch('openai.ChatCompletion.acreate', mock_openai_create)

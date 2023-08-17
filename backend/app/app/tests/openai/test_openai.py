import pytest
from unittest import mock

# from openai_manager import OpenAiManager
from app.openai.base import *
from app.openai.core import *


@pytest.fixture
def openai_manager():
    return OpenAiManager()


def test_get_completion(openai_manager):
    prompt = "Hello"

    response = openai_manager.get_completion(prompt)

    # assert response.status == 200
    assert response is not None


def test_get_chat_completion(openai_manager):
    prompt = "Hello, world!"

    response = openai_manager.get_chat_completion(prompt)
    assert response is not None


def test_get_embedding(openai_manager):
    prompt = "Hello, world!"
    expected_embedding = [0.1, 0.2, 0.3]

    with mock.patch("openai.Embedding.create") as mock_create:
        mock_create.return_value = {"data": [{"embedding": expected_embedding}]}

        embedding = openai_manager.get_embedding(prompt)

    assert embedding == expected_embedding
    mock_create.assert_called_once_with(input=[prompt], model="text-embedding-ada-002")


def test_get_embeddings(openai_manager):
    prompts = ["Prompt 1", "Prompt 2"]
    expected_embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]

    with mock.patch("openai.Embedding.create") as mock_create:
        mock_create.return_value = {
            "data": [
                {"embedding": expected_embeddings[0]},
                {"embedding": expected_embeddings[1]},
            ]
        }

        embeddings = openai_manager.get_embeddings(prompts)

    assert embeddings == expected_embeddings
    mock_create.assert_called_once_with(input=prompts, model="text-embedding-ada-002")

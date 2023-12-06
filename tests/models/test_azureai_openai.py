import os

import pytest

from guidance import models, gen, system, user, assistant


def _env_or_skip(var_name: str) -> str:
    env_value = os.getenv(var_name, None)

    if env_value is None:
        pytest.skip(f"Did not find required environment variable: {var_name}")
    return env_value


def test_azureai_openai_chat_smoke():
    azureai_endpoint = _env_or_skip("AZUREAI_CHAT_ENDPOINT")
    azureai_key = _env_or_skip("AZUREAI_CHAT_KEY")
    model = _env_or_skip("AZUREAI_CHAT_MODEL")

    lm = models.AzureOpenAI(
        model=model, azure_endpoint=azureai_endpoint, api_key=azureai_key
    )
    assert isinstance(lm, models.AzureOpenAIChat)

    with system():
        lm += "You are a math wiz."

    with user():
        lm += "What is 1 + 1?"

    with assistant():
        lm += gen(max_tokens=10, name="text")
        lm += "Pick a number: "

    print(lm)
    assert len(lm["text"]) > 0


def test_azureai_openai_completion_smoke():
    azureai_endpoint = _env_or_skip("AZUREAI_COMPLETION_ENDPOINT")
    azureai_key = _env_or_skip("AZUREAI_COMPLETION_KEY")
    model = _env_or_skip("AZUREAI_COMPLETION_MODEL")

    lm = models.AzureOpenAI(
        model=model, azure_endpoint=azureai_endpoint, api_key=azureai_key
    )
    assert isinstance(lm, models.AzureOpenAICompletion)

    result = f"{lm}What is 2+2?" + gen(max_tokens=10, name="text")
    print(f"result: {result['text']}")
    assert len(result["text"]) > 0

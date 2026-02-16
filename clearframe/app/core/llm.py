from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """
    Provider-agnostic LLM interface.

    Engine never knows which provider is used.
    """

    @abstractmethod
    def consult_sunk_cost(self, text: str) -> str:
        """
        Returns reasoning string only.
        Must never raise.
        """
        raise NotImplementedError


# ------------------------------------------------------------------
# Mock Client (used for tests + fallback)
# ------------------------------------------------------------------

class MockLLMClient(LLMClient):
    def consult_sunk_cost(self, text: str) -> str:
        return "Mock analysis: possible sunk cost reasoning detected."


# ------------------------------------------------------------------
# OpenAI Client
# ------------------------------------------------------------------

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def consult_sunk_cost(self, text: str) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze for sunk cost reasoning."},
                    {"role": "user", "content": text},
                ],
                temperature=0,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"LLM_ERROR: {e}"


# ------------------------------------------------------------------
# Anthropic Client
# ------------------------------------------------------------------

class AnthropicClient(LLMClient):
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def consult_sunk_cost(self, text: str) -> str:
        try:
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0,
                messages=[
                    {"role": "user", "content": f"Analyze for sunk cost reasoning:\n{text}"}
                ],
            )
            return msg.content[0].text.strip()
        except Exception as e:
            return f"LLM_ERROR: {e}"


# ------------------------------------------------------------------
# Factory
# ------------------------------------------------------------------

def get_llm(provider: Optional[str] = None) -> LLMClient:
    """
    Environment-driven provider selection.

    CLEARFRAME_LLM_PROVIDER=openai | anthropic | mock
    """

    provider = provider or os.getenv("CLEARFRAME_LLM_PROVIDER", "mock").lower()

    if provider == "openai":
        return OpenAIClient()

    if provider == "anthropic":
        return AnthropicClient()

    return MockLLMClient()

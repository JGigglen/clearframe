from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """
    Provider-agnostic LLM interface.
    The Engine never knows which provider is used.
    """

    @abstractmethod
    def consult_sunk_cost(self, text: str) -> str:
        """
        Returns reasoning string only.
        Must never raise.
        """
        raise NotImplementedError


# ------------------------------------------------------------------
# Mock Client (Deterministic Fallback)
# ------------------------------------------------------------------

class MockLLMClient(LLMClient):
    def consult_sunk_cost(self, text: str) -> str:
        return "Mock analysis: possible sunk cost reasoning detected."


# ------------------------------------------------------------------
# Gemini Client (Google) - YOUR NEW ADDITION
# ------------------------------------------------------------------

class GeminiClient(LLMClient):
    # Constitutional Rule: Use the proven, stable model version
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)

    def consult_sunk_cost(self, text: str) -> str:
        if not self.model:
            return "LLM_ERROR: GOOGLE_API_KEY not set in environment."
        try:
            # Temperature 0 for deterministic reasoning
            response = self.model.generate_content(
                f"Analyze the following text for sunk cost reasoning. Be concise:\n\n{text}",
                generation_config={"temperature": 0}
            )
            return response.text.strip()
        except Exception as e:
            return f"LLM_ERROR: {str(e)}"


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
# Factory
# ------------------------------------------------------------------

def get_llm(provider: Optional[str] = None) -> LLMClient:
    """
    Environment-driven provider selection.
    Set CLEARFRAME_LLM_PROVIDER=gemini | openai | anthropic | mock
    """

    provider = provider or os.getenv("CLEARFRAME_LLM_PROVIDER", "mock").lower()

    if provider == "gemini":
        return GeminiClient()

    if provider == "openai":
        return OpenAIClient()

    # Fallback to Mock if nothing
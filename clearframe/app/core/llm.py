import os
import json
from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def consult_sunk_cost(self, text: str) -> str:
        pass

    @abstractmethod
    def reframe_sunk_cost(self, engine_data: dict) -> dict:
        pass

class GeminiClient(LLMClient):
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
            return "LLM_ERROR: No API key found."
        try:
            response = self.model.generate_content(
                f"Analyze the following text for sunk-cost bias. Explain why or why not: {text}"
            )
            return response.text
        except Exception as e:
            return f"LLM_ERROR: {str(e)}"

    def reframe_sunk_cost(self, engine_data: dict) -> dict:
        if not self.model:
            return {"counterfactual": None, "rationale": "No API key."}
        
        prompt = (
            "You are ClearframeReframe. Goal: produce a single counterfactual frame for sunk-cost bias.\n"
            "Rules:\n"
            "- Do NOT give advice. Do NOT recommend actions. Do NOT moralize.\n"
            "- Output MUST be valid JSON only.\n"
            "- Ensure the JSON keys are exactly 'counterfactual' and 'rationale' (lowercase).\n"
            "- Provide exactly ONE counterfactual question < 25 words.\n"
            "- The question must remove past investment from the reasoning.\n"
            f"\nInput JSON: {json.dumps(engine_data)}"
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            return {"counterfactual": None, "rationale": f"Reframer Error: {str(e)}"}

class MockClient(LLMClient):
    def consult_sunk_cost(self, text: str) -> str:
        return "MOCK_ANALYSIS: Sunk cost detected (Simulated)."
    
    def reframe_sunk_cost(self, engine_data: dict) -> dict:
        return {"counterfactual": "MOCK: If today was day one, would you start?", "rationale": "Mock output."}

def get_llm():
    provider = os.getenv("CLEARFRAME_LLM_PROVIDER", "mock").lower()
    if provider == "gemini":
        return GeminiClient()
    return MockClient()
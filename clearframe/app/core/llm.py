import os
import json
from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def analyze_bias(self, text: str, bias_type: str) -> str:
        pass

    @abstractmethod
    def generate_reframe(self, engine_data: dict) -> dict:
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

    def analyze_bias(self, text: str, bias_type: str) -> str:
        """Narrative analysis specialized by bias type."""
        if not self.model: return "LLM_ERROR: No API key."
        
        prompts = {
            "SUNK_COST": f"Analyze this text for Sunk-Cost Fallacy (continuing failing effort due to past investment): {text}",
            "CONFIRMATION_BIAS": f"Analyze this text for Confirmation Bias (seeking info that confirms pre-existing beliefs while ignoring contradictions): {text}",
            "UNKNOWN": f"Analyze this text for general cognitive bias or logical fallacies: {text}"
        }
        
        prompt = prompts.get(bias_type, prompts["UNKNOWN"])
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"LLM_ERROR: {str(e)}"

    def generate_reframe(self, engine_data: dict) -> dict:
        """The 'Clearframe' move: JSON-only counterfactual generation."""
        if not self.model: return {"counterfactual": None, "rationale": "No API key."}
        
        bias_type = engine_data.get("bias_context", "SUNK_COST")
        text = engine_data.get("text", "")

        # Specialized instructions per bias
        reframer_rules = {
            "SUNK_COST": "Remove all past investment (time/money) from the choice. Focus only on future cost vs future benefit.",
            "CONFIRMATION_BIAS": "Create a frame that forces the user to argue for the OPPOSITE of their current conclusion."
        }
        
        rule = reframer_rules.get(bias_type, "Create a neutral counterfactual that challenges the primary assumption.")

        prompt = (
            f"You are ClearframeReframe for {bias_type}. Output valid JSON ONLY.\n"
            f"Rule: {rule}\n"
            "- Exactly ONE question < 25 words.\n"
            "- Keys: 'counterfactual', 'rationale' (lowercase).\n"
            f"Input: {text}"
        )

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            return {"counterfactual": None, "rationale": f"Reframer Error: {str(e)}"}

def get_llm():
    if os.getenv("CLEARFRAME_LLM_PROVIDER") == "gemini":
        return GeminiClient()
    return MockClient()

class MockClient(LLMClient):
    def analyze_bias(self, text, bias_type): return f"MOCK: {bias_type} detected."
    def generate_reframe(self, data): return {"counterfactual": "Mock?", "rationale": "Mock."}
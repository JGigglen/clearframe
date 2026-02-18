import os
import json
from abc import ABC, abstractmethod
from google import genai # The new 2026 standard

class LLMClient(ABC):
    @abstractmethod
    def analyze_bias(self, text: str, bias_type: str) -> str:
        pass

    @abstractmethod
    def generate_reframe(self, engine_data: dict) -> dict:
        pass

class GeminiClient(LLMClient):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.client = None
        else:
            # Modern 2026 SDK initialization
            self.client = genai.Client(api_key=api_key)
            self.model_name = model_name

    def analyze_bias(self, text: str, bias_type: str) -> str:
        if not self.client: return "LLM_ERROR: No API key."
        
        prompts = {
            "SUNK_COST": f"Analyze for Sunk-Cost Fallacy: {text}",
            "CONFIRMATION_BIAS": f"Analyze for Confirmation Bias: {text}",
            "UNKNOWN": f"Analyze for general cognitive bias: {text}"
        }
        
        prompt = prompts.get(bias_type, prompts["UNKNOWN"])
        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            return response.text
        except Exception as e:
            return f"LLM_ERROR: {str(e)}"

    def generate_reframe(self, engine_data: dict) -> dict:
        if not self.client: return {"counterfactual": None, "rationale": "No API key."}
        
        bias_type = engine_data.get("bias_context", "SUNK_COST")
        text = engine_data.get("text", "")
        
        reframer_rules = {
            "SUNK_COST": "Focus only on future cost vs future benefit.",
            "CONFIRMATION_BIAS": "Force the user to argue for the OPPOSITE of their conclusion."
        }
        
        rule = reframer_rules.get(bias_type, "Create a neutral counterfactual.")

        prompt = (
            f"Output valid JSON ONLY. Rule: {rule}\n"
            "- Exactly ONE question < 25 words.\n"
            "- Keys: 'counterfactual', 'rationale'.\n"
            f"Input: {text}"
        )

        try:
            # New 2026 structured output syntax
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            return json.loads(response.text)
        except Exception as e:
            return {"counterfactual": None, "rationale": f"Reframer Error: {str(e)}"}

def get_llm():
    if os.getenv("CLEARFRAME_LLM_PROVIDER") == "gemini":
        return GeminiClient()
    return MockClient()

class MockClient(LLMClient):
    def analyze_bias(self, text: str, bias_type: str) -> str:
        # Instead of a hardcoded string, use the bias_type passed in!
        return f"MOCK: {bias_type} detected."

    def generate_reframe(self, engine_data: dict) -> dict:
        # Echo the bias type back in the rationale
        bias = engine_data.get("bias_context", "UNKNOWN")
        return {
            "counterfactual": f"What if you ignored the {bias} and looked at the long-term data?",
            "rationale": f"Mocking a {bias} reframe."
        }
import os
import json
import time

class LLMClient:
    def analyze_bias(self, text: str, bias_type: str) -> str:
        raise NotImplementedError
        
    def generate_reframe(self, analysis: dict) -> dict:
        raise NotImplementedError

class MockClient(LLMClient):
    def analyze_bias(self, text: str, bias_type: str) -> str:
        return f"MOCK ANALYSIS: Strong signal for {bias_type} detected in text."

    def generate_reframe(self, analysis: dict) -> dict:
        return {
            "rationale": "MOCK: Logic appears circular.",
            "counterfactual": "How would you view this decision if you had zero prior investment?"
        }

class GeminiClient(LLMClient):
    def __init__(self, api_key: str):
        # Lazy Import: Only fails if you actually try to use Gemini
        try:
            from google import genai
            self.client = genai.Client(api_key=api_key)
        except ImportError:
            raise ImportError("Gemini library not found. Run 'pip install google-genai'")
            
    def analyze_bias(self, text: str, bias_type: str) -> str:
        # (This remains the same as before, simplified for the fix)
        return "GEMINI ANALYSIS PLACEHOLDER"

    def generate_reframe(self, analysis: dict) -> dict:
        return {"rationale": "Gemini Placeholder", "counterfactual": "Gemini Question?"}

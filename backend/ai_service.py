# /backend/ai_service.py
import os
import openai
from config import Config

def generate_code_snippet(user_idea, template_type, provider="openai"):
    prompt = f"""
    You are an expert Chrome extension developer AI.
    The user wants a {template_type} extension. The idea: {user_idea}.
    Generate a concise, self-contained JS snippet for background.js with inline comments explaining logic.
    """
    if provider == "openai":
        openai.api_key = Config.OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=500, temperature=0.7
        )
        code = response.choices[0].text.strip()
        return code
    # Add other providers similarly
    return "// fallback code"

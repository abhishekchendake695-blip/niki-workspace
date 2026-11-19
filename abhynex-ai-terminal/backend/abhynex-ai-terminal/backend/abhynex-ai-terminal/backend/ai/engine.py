import os
import google.generativeai as genai
from groq import Groq
from typing import List, Dict, Any

class AIEngine:
    def __init__(self, provider='gemini', api_key=None):
        self.provider = provider
        self.api_key = api_key
        if provider == 'gemini' and api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        elif provider == 'groq' and api_key:
            self.client = Groq(api_key=api_key)

    async def generate_response(self, prompt: str, history: List[Dict] = []) -> str:
        if not self.api_key: return "API Key missing"
        try:
            if self.provider == 'gemini':
                chat = self.model.start_chat(history=[{'role': h['role'], 'parts': [h['content']]} for h in history])
                response = chat.send_message(prompt)
                return response.text
            elif self.provider == 'groq':
                messages = history + [{'role': 'user', 'content': prompt}]
                completion = self.client.chat.completions.create(
                    model='llama-3.3-70b-versatile',
                    messages=messages
                )
                return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
        return 'Unsupported provider'
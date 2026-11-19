import os
import google.generativeai as genai
from groq import Groq
from typing import List, Dict, Any

class AIEngine:
    def __init__(self, provider='gemini', api_key=None):
        self.provider = provider
        self.api_key = api_key
        if provider == 'gemini':
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        elif provider == 'groq':
            self.client = Groq(api_key=api_key)

    async def generate_response(self, prompt: str, history: List[Dict] = []) -> str:
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
        return 'Unsupported provider'
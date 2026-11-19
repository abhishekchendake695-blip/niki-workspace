from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils.shell import run_command
from utils.files import list_files, read_file, write_file, delete_path
from ai.engine import AIEngine
from ai.agent import AIAgent
import os

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    provider: str = 'gemini'
    api_key: str

class AgentRequest(BaseModel):
    instruction: str
    provider: str = 'gemini'
    api_key: str

@router.post('/chat')
async def chat(req: ChatRequest):
    try:
        engine = AIEngine(provider=req.provider, api_key=req.api_key)
        response = await engine.generate_response(req.message, req.history)
        return {'response': response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/agent/run')
async def run_agent(req: AgentRequest):
    try:
        agent = AIAgent(provider=req.provider, api_key=req.api_key)
        result = await agent.execute(req.instruction)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/files')
def get_files(path: str = '.'):
    return list_files(path)

@router.post('/files/write')
def save_file(path: str, content: str):
    write_file(path, content)
    return {'status': 'success'}

@router.get('/files/read')
def get_file_content(path: str):
    return {'content': read_file(path)}
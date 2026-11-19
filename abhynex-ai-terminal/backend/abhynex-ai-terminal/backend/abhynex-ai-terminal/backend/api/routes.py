from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from utils.shell import ShellExecutor
from utils.files import FileManager
from ai.engine import AIEngine
from ai.agent import AIAgent

router = APIRouter()
shell = ShellExecutor()
files = FileManager()

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    provider: str = 'gemini'
    api_key: str

class CommandRequest(BaseModel):
    command: str

@router.post('/chat')
async def chat(req: ChatRequest):
    engine = AIEngine(provider=req.provider, api_key=req.api_key)
    response = await engine.generate_response(req.message, req.history)
    return {'response': response}

@router.post('/agent/run')
async def run_agent(req: ChatRequest):
    agent = AIAgent(provider=req.provider, api_key=req.api_key)
    result = await agent.execute_task(req.message)
    return result

@router.post('/terminal/run')
def run_cmd(req: CommandRequest):
    return shell.execute(req.command)

@router.get('/files')
def get_files(path: str = '.'):
    return {'files': files.list_files(path)}

import os
import sqlite3
import subprocess
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("abhynex-backend")

app = FastAPI(title="ABHYNEX AI TERMINAL Backend", version="1.0.0")
router = APIRouter(prefix="/api/v1")

DB_FILE = "abhynex_backend.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS terminal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            command TEXT,
            output TEXT,
            exit_code INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kv_store (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class CommandRequest(BaseModel):
    session_id: str = "default"
    command: str

class CommandResponse(BaseModel):
    session_id: str
    command: str
    output: str
    exit_code: int

class FileWriteRequest(BaseModel):
    path: str
    content: str

class FileItem(BaseModel):
    name: str
    path: str
    is_directory: bool
    size: int

@router.post("/terminal/exec", response_model=CommandResponse)
async def execute_command(req: CommandRequest):
    logger.info(f"Executing command in session {req.session_id}: {req.command}")
    try:
        process = subprocess.run(
            req.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        stdout = process.stdout
        stderr = process.stderr
        output = stdout + stderr
        exit_code = process.returncode
    except subprocess.TimeoutExpired:
        output = "Error: Command timed out after 60 seconds."
        exit_code = -1
    except Exception as e:
        output = f"Error executing command: {str(e)}"
        exit_code = -1

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO terminal_logs (session_id, command, output, exit_code) VALUES (?, ?, ?, ?)",
            (req.session_id, req.command, output, exit_code)
        )
        conn.commit()
        conn.close()
    except Exception as db_err:
        logger.error(f"Failed to persist terminal log: {db_err}")

    return CommandResponse(
        session_id=req.session_id,
        command=req.command,
        output=output,
        exit_code=exit_code
    )

@router.get("/files/list", response_model=List[FileItem])
async def list_files(path: str = "."):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Path not found")
    
    items = []
    try:
        for entry in os.scandir(path):
            stat = entry.stat()
            items.append(FileItem(
                name=entry.name,
                path=entry.path,
                is_directory=entry.is_dir(),
                size=stat.st_size
            ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return items

@router.post("/files/write")
async def write_file(req: FileWriteRequest):
    try:
        directory = os.path.dirname(req.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        async with aiofiles.open(req.path, "w", encoding="utf-8") as f:
            await f.write(req.content)
        return {"status": "success", "path": req.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/read")
async def read_file(path: str):
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "abhynex-backend"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

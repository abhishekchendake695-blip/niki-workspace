import json
from typing import List, Dict, Any
from .engine import AIEngine
from ..utils.shell import ShellExecutor
from ..utils.files import FileManager

class AIAgent:
    def __init__(self):
        self.engine = AIEngine()
        self.shell = ShellExecutor()
        self.files = FileManager()
        self.memory = []

    async def execute_task(self, instruction: str):
        # 1. Plan
        plan_prompt = f"Task: {instruction}\nCreate a step-by-step plan to achieve this. Return as JSON list of steps."
        plan_response = await self.engine.generate_response(plan_prompt)
        
        # 2. Execute steps (simplified for now)
        results = []
        steps = [instruction] # Fallback to single step if parsing fails
        try:
            steps = json.loads(plan_response)
        except:
            pass

        for step in steps:
            # Determine tool
            tool_prompt = f"Step: {step}\nWhich tool to use? (shell, file, none). Return only the tool name."
            tool = await self.engine.generate_response(tool_prompt)
            tool = tool.strip().lower()

            if 'shell' in tool:
                cmd_prompt = f"Step: {step}\nProvide the shell command to execute. Return only the command."
                cmd = await self.engine.generate_response(cmd_prompt)
                res = self.shell.execute(cmd.strip())
                results.append(res)
            elif 'file' in tool:
                # Simplified file logic
                results.append({'status': 'file operation requested'})
            else:
                results.append({'status': 'no tool used'})

        return {"instruction": instruction, "plan": steps, "results": results}
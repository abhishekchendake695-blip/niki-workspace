import json
from .engine import AIEngine
from ..utils.shell import ShellExecutor
from ..utils.files import FileManager

class AIAgent:
    def __init__(self, provider='gemini', api_key=None):
        self.engine = AIEngine(provider, api_key)
        self.shell = ShellExecutor()
        self.files = FileManager()

    async def execute_task(self, instruction: str):
        plan_prompt = f"Task: {instruction}\nCreate a step-by-step plan. Return ONLY a JSON list of strings."
        plan_response = await self.engine.generate_response(plan_prompt)
        
        try:
            steps = json.loads(plan_response)
        except:
            steps = [instruction]

        results = []
        for step in steps:
            tool_prompt = f"Step: {step}\nTool? (shell/file/none). Return one word."
            tool = (await self.engine.generate_response(tool_prompt)).strip().lower()

            if 'shell' in tool:
                cmd = (await self.engine.generate_response(f"Command for: {step}. Return ONLY command.")).strip()
                results.append(self.shell.execute(cmd))
            else:
                results.append({"step": step, "status": "completed"})

        return {"plan": steps, "results": results}
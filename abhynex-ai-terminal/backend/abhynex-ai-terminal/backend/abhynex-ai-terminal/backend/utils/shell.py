import subprocess

class ShellExecutor:
    def execute(self, command: str):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            }
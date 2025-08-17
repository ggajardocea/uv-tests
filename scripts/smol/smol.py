from smolagents import CodeAgent, MLXModel, tool
from subprocess import run
import sys

@tool
def write_file(path: str, content: str) -> str:
    """Write text.
    Args:
      path (str): File path.
      content (str): Text to write.
    Returns:
      str: Status.
    """
    try:
        open(path, "w", encoding="utf-8").write(content)
        return f"saved:{path}"
    except Exception as e:
        return f"error:{e}"

@tool
def sh(cmd: str) -> str:
    """Run a shell command.
    Args:
      cmd (str): Command to execute.
    Returns:
      str: stdout+stderr.
    """
    try:
        r = run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout + r.stderr
    except Exception as e:
        return f"error:{e}"

if __name__ == "__main__":
    print("que paza")
    if len(sys.argv) < 2:
        print("usage: python agent.py 'your prompt'"); sys.exit(1)
    common = "use cat/head to read files, use rg to search, use ls and standard shell commands to explore."
    agent = CodeAgent(
        model=MLXModel(model_id="mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit-dwq-v2", max_tokens=8192, trust_remote_code=True),
        tools=[write_file, sh],
        add_base_tools=True,
    )
    print(dir(agent))
    print(agent.run(" ".join(sys.argv[1:]) + " " + common))
    
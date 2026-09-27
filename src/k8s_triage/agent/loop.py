import os
from typing import Any

from openai import OpenAI
from rich.console import Console

from k8s_triage.agent.prompts import SYSTEM_PROMPT
from k8s_triage.agent.tools import execute_tool, get_openai_tools
from k8s_triage.config import config

console = Console()

class AgentController:
    def __init__(self) -> None:
        api_key = config.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be provided via K8S_TRIAGE_OPENAI_API_KEY or OPENAI_API_KEY env var.")
        self.client = OpenAI(api_key=api_key)
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.tools = get_openai_tools()

    def run(self, prompt: str) -> str:
        self.messages.append({"role": "user", "content": prompt})
        
        iterations = 0
        with console.status("[bold green]Agent is analyzing the cluster...", spinner="dots") as status:
            while iterations < config.max_tool_iterations:
                iterations += 1
                
                # Use type ignore to bypass strict message typing
                response = self.client.chat.completions.create(
                    model=config.model,
                    messages=self.messages, # type: ignore
                    tools=self.tools,
                    tool_choice="auto"
                )
                
                msg = response.choices[0].message
                
                if msg.tool_calls:
                    self.messages.append(msg.model_dump(exclude_none=True))
                    
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = tool_call.function.arguments
                        
                        status.update(f"[bold cyan][Tool] Running {tool_name}...")
                        result = execute_tool(tool_name, tool_args)
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result
                        })
                else:
                    self.messages.append({"role": "assistant", "content": msg.content})
                    return msg.content or "No response content."
            
            return "Agent stopped: Reached maximum tool iterations limit."

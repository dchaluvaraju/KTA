import json
from typing import Any

from pydantic import BaseModel, Field

from k8s_triage.k8s import operations


class ListNamespacesArgs(BaseModel):
    pass

class ListPodsArgs(BaseModel):
    namespace: str = Field(..., description="The Kubernetes namespace to list pods for")

class GetPodLogsArgs(BaseModel):
    namespace: str = Field(..., description="Namespace of the pod")
    pod_name: str = Field(..., description="Name of the pod")
    container_name: str | None = Field(None, description="Optional name of the container")
    tail_lines: int | None = Field(None, description="Number of lines from the end of the logs to show")
    previous: bool = Field(False, description="If true, return previous terminated container logs")

class GetEventsArgs(BaseModel):
    namespace: str = Field(..., description="Namespace to get events from")
    involved_object_name: str | None = Field(None, description="Optional filter for specific object name")

class GetNodeStatusArgs(BaseModel):
    pass

# We can define the tools registry
TOOLS_REGISTRY: dict[str, dict[str, Any]] = {
    "list_namespaces": {
        "function": operations.list_namespaces,
        "schema": ListNamespacesArgs,
        "description": "List all namespaces in the cluster."
    },
    "list_pods_with_conditions": {
        "function": operations.list_pods_with_conditions,
        "schema": ListPodsArgs,
        "description": "List pods in a namespace along with their status, conditions, and container statuses."
    },
    "get_pod_logs": {
        "function": operations.get_pod_logs,
        "schema": GetPodLogsArgs,
        "description": "Retrieve logs for a specific pod/container. Output is sanitized and truncated to prevent token overflow."
    },
    "get_namespaced_events": {
        "function": operations.get_namespaced_events,
        "schema": GetEventsArgs,
        "description": "Get recent events in a namespace, optionally filtered by an object's name."
    },
    "get_node_status": {
        "function": operations.get_node_status,
        "schema": GetNodeStatusArgs,
        "description": "Get the status and conditions of all nodes in the cluster."
    }
}

def get_openai_tools() -> list[dict[str, Any]]:
    """Generate strict OpenAI tool definitions from the registry."""
    tools = []
    for name, metadata in TOOLS_REGISTRY.items():
        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": metadata["description"],
                "parameters": metadata["schema"].model_json_schema(),
                "strict": True
            }
        })
    return tools

def execute_tool(name: str, arguments: str) -> str:
    """Execute a tool by name with JSON string arguments."""
    if name not in TOOLS_REGISTRY:
        return f"Error: Tool {name} not found."
    
    try:
        args_dict = json.loads(arguments)
        # Validate with pydantic
        schema_cls = TOOLS_REGISTRY[name]["schema"]
        validated_args = schema_cls(**args_dict)
        
        # Execute function
        func = TOOLS_REGISTRY[name]["function"]
        result = func(**validated_args.model_dump())
        
        if isinstance(result, str):
            return result
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error executing tool {name}: {e!s}"

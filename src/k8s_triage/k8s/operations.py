from typing import Any

from kubernetes.client.rest import ApiException

from k8s_triage.config import config
from k8s_triage.k8s.client import get_core_v1_api
from k8s_triage.k8s.sanitizer import process_logs


def list_namespaces() -> list[str]:
    """List all namespaces in the cluster."""
    try:
        api = get_core_v1_api()
        namespaces = api.list_namespace()
        return [ns.metadata.name for ns in namespaces.items if ns.metadata]
    except ApiException as e:
        return [f"Error listing namespaces: {e}"]

def list_pods_with_conditions(namespace: str) -> list[dict[str, Any]]:
    """List pods in a namespace with their statuses and conditions."""
    try:
        api = get_core_v1_api()
        pods = api.list_namespaced_pod(namespace)
        result = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "conditions": [
                    {"type": c.type, "status": c.status, "reason": c.reason, "message": c.message}
                    for c in (pod.status.conditions or [])
                ],
                "container_statuses": [
                    {
                        "name": cs.name,
                        "ready": cs.ready,
                        "restart_count": cs.restart_count,
                        "state": cs.state.to_dict() if cs.state else None,
                    }
                    for cs in (pod.status.container_statuses or [])
                ]
            }
            result.append(pod_info)
        return result
    except ApiException as e:
        return [{"error": f"Error listing pods in namespace {namespace}: {e}"}]

def get_pod_logs(namespace: str, pod_name: str, container_name: str | None = None, tail_lines: int | None = None, previous: bool = False) -> str:
    """Retrieve logs for a specific pod/container, sanitized and truncated."""
    try:
        api = get_core_v1_api()
        lines = tail_lines if tail_lines is not None else config.max_log_lines
        lines = min(lines, config.max_log_lines_cap)
        
        kwargs = {
            "namespace": namespace,
            "name": pod_name,
            "tail_lines": lines,
            "previous": previous
        }
        if container_name:
            kwargs["container"] = container_name
            
        logs = api.read_namespaced_pod_log(**kwargs)
        return process_logs(logs)
    except ApiException as e:
        return f"Error retrieving logs for {pod_name}: {e}"

def get_namespaced_events(namespace: str, involved_object_name: str | None = None) -> list[dict[str, Any]]:
    """Get recent events in a namespace, optionally filtered by object name."""
    try:
        api = get_core_v1_api()
        field_selector = f"involvedObject.name={involved_object_name}" if involved_object_name else None
        
        events = api.list_namespaced_event(namespace, field_selector=field_selector)
        
        result = []
        for event in events.items:
            result.append({
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "object": event.involved_object.name,
                "count": event.count,
                "last_timestamp": event.last_timestamp.isoformat() if event.last_timestamp else None
            })
        
        # Sort by timestamp, most recent last
        result.sort(key=lambda x: x["last_timestamp"] or "")
        return result[-20:] # Return last 20 events
    except ApiException as e:
        return [{"error": f"Error retrieving events: {e}"}]

def get_node_status() -> list[dict[str, Any]]:
    """Describe cluster nodes and their conditions."""
    try:
        api = get_core_v1_api()
        nodes = api.list_node()
        result = []
        for node in nodes.items:
            result.append({
                "name": node.metadata.name,
                "conditions": [
                    {"type": c.type, "status": c.status, "reason": c.reason, "message": c.message}
                    for c in (node.status.conditions or [])
                ]
            })
        return result
    except ApiException as e:
        return [{"error": f"Error listing nodes: {e}"}]

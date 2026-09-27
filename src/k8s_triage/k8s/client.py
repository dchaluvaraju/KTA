from kubernetes import client
from kubernetes import config as k8s_config


def load_k8s_config() -> None:
    """Load Kubernetes configuration (in-cluster or local)."""
    try:
        # Try in-cluster first
        k8s_config.load_incluster_config()
    except k8s_config.config_exception.ConfigException:
        # Fallback to local kubeconfig
        try:
            k8s_config.load_kube_config()
        except k8s_config.config_exception.ConfigException:
            # Maybe raise or handle it if neither works
            pass

def get_core_v1_api() -> client.CoreV1Api:
    load_k8s_config()
    return client.CoreV1Api()

def get_apps_v1_api() -> client.AppsV1Api:
    load_k8s_config()
    return client.AppsV1Api()

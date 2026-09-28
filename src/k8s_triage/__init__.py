"""Kubernetes Triage Assistant (k8s-triage-agent)."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("k8s-triage-assistant")
except PackageNotFoundError:
    __version__ = "0.1.1"

__all__ = ["__version__"]

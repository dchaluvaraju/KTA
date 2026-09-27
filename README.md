# Kubernetes Triage Assistant (`k8s-triage-agent`)

![KTA Logo](docs/logo.jpg)

A production-ready, autonomous CLI and service daemon that inspects, analyzes, and troubleshoots Kubernetes cluster issues using the OpenAI SDK tool-calling paradigm.

## Features
- **Read-Only Inspection**: Safely queries the cluster without mutation permissions.
- **Automated Root Cause Analysis**: Identifies failing pods, correlates events, and analyzes logs.
- **Security & Guardrails**: Includes log truncation to protect LLM context windows and redacts sensitive information (secrets, tokens, passwords).
- **Interactive CLI**: Typer/Rich based CLI for beautiful formatting and easy interaction.

## Installation

```bash
uv venv
source .venv/bin/activate
pip install -e .
```

## Usage

Export your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
# Or use the K8S_TRIAGE_ prefix
export K8S_TRIAGE_OPENAI_API_KEY="sk-..."
```

Run an analysis:
```bash
k8s-triage analyze --namespace default --pod my-crashing-pod
```

Start interactive mode:
```bash
k8s-triage interactive
```

## Testing

```bash
pytest tests/
```

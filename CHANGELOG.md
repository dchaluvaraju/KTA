# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-27

### Added
- Core autonomous ReAct agent loop supporting OpenAI tool calling.
- Read-only Kubernetes adapter for inspecting pods, namespaces, conditions, logs, and events.
- Secret and PII sanitizer scrubbing tokens, JWTs, private keys, and passwords.
- Context window protection enforcing log truncation and line limits.
- Rich CLI interface powered by Typer and Rich (`analyze` and `interactive` modes).
- `--version` and `--help` CLI flags.
- Kubernetes RBAC manifest (`config/rbac-readonly.yaml`) with least-privilege read-only permissions.
- Continuous Integration (CI) pipeline testing on Python 3.11 and 3.12.
- Automated release workflow for tagged versions (`v*.*.*`).

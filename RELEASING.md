# Release Process & Versioning Standards

This document describes the release workflow and versioning standards for `k8s-triage-assistant` (`KTA`).

---

## 1. Versioning Standards: Semantic Versioning (SemVer 2.0.0)

Version numbers follow the standard **`MAJOR.MINOR.PATCH`** convention:

- **`MAJOR` (e.g., `1.0.0`)**: Incompatible API or CLI breaking changes, major paradigm shifts.
- **`MINOR` (e.g., `0.2.0`)**: Backwards-compatible new features (e.g., new diagnostic tools, new Kubernetes resource adapters, new LLM providers).
- **`PATCH` (e.g., `0.1.1`)**: Backwards-compatible bug fixes, security patches (e.g., regex scrubber improvements, token guard updates).

### Single Source of Truth
The version is defined in:
1. `pyproject.toml` (`version = "X.Y.Z"`)
2. Read dynamically at runtime via `k8s_triage.__version__` (`importlib.metadata`)
3. Displayed in CLI via `k8s-triage --version`

---

## 2. Release Flow Overview

We use **Tag-Driven Automated Releases**:

```
 [Feature Branch] -> PR -> CI (Lint, Typecheck, Test) -> Merge to main
                                                              |
                                                    Update Version & Changelog
                                                              |
                                                      Git Tag (vX.Y.Z)
                                                              |
                                                       Push Tag to GitHub
                                                              |
                                              GitHub Actions Release Workflow:
                                              1. Validates tests & linting
                                              2. Builds wheels & source dist
                                              3. Publishes GitHub Release
```

---

## 3. Step-by-Step Release Instructions

### Step 1: Prepare the Release
1. Update `version` in `pyproject.toml`:
   ```toml
   [project]
   version = "0.2.0"
   ```
2. Update `CHANGELOG.md`:
   - Move entries under `[Unreleased]` into a new section `## [0.2.0] - YYYY-MM-DD`.

### Step 2: Commit and Merge to `main`
```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): prepare v0.2.0"
git push origin main
```

### Step 3: Create and Push Git Tag
Tag the commit with the standard `v` prefix matching SemVer:
```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

### Step 4: Automated CI/CD Execution
Once the tag is pushed:
1. The **Release Workflow** (`.github/workflows/release.yaml`) triggers automatically.
2. It builds the distribution packages (`.whl` and `.tar.gz`).
3. It creates a **GitHub Release** with auto-generated release notes and attached distribution assets.

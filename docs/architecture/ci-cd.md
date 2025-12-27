# CI/CD Architecture – TradingBot

This document describes the Continuous Integration (CI) pipeline used in the TradingBot project.
The CI pipeline is designed to enforce **security**, **code quality**, and **correctness** before
any code is merged into the `main` branch.

The pipeline is implemented using **Azure DevOps Pipelines** and defined in:

## 1. Goals of the CI Pipeline

The CI pipeline is designed to:

- Prevent secret leakage (API keys, tokens, credentials)
- Enforce consistent code formatting and style
- Catch bugs early via linting and static typing
- Ensure tests exist and meet minimum coverage
- Detect vulnerable third-party dependencies
- Ensure the Docker image can always be built

The pipeline follows a **fail-fast** philosophy: if any step fails, the pipeline stops.

---


## 2. Pipeline Triggers

The pipeline runs automatically on:

- Pushes to the `main` branch
- Pull requests targeting the `main` branch

```yaml
trigger:
  branches:
    include:
      - main

pr:
  branches:
    include:
      - main
```

This ensures that:
- main is always protected
- Pull requests must pass CI before merging
- The pipeline runs on both direct commits and pull requests

The pipeline uses a Linux build agent:
```yaml
pool:
  vmImage: ubuntu-latest
```
Python version and tool versions are defined as variables to keep things explicit and reproducible.

## 3. Execution Environment

- OS: ubuntu-latest
- Python: 3.11
- Build agent: Azure-hosted Linux VM

All tooling versions are pinned or explicitly installed during the pipeline.

### 4. CI checks
Various automated checks are included in the pipeline:
- Secret Scanning – gitleaks
- Code Formatting – ruff format
- Linting – ruff check
- Type Checking – mypy
- Tests & Coverage – pytest
- Docker Build Validation

### 4.1. Secret Scanning – gitleaks
**What it does**

```gitleaks``` scans the entire Git history for secrets such as:
- API keys
- Tokens
- Passwords
- Private keys

The pipeline performs a full-history scan using:

```bash
gitleaks detect \
  --redact \
  --config .gitleaks.toml \
  --report-format sarif \
  --report-path gitleaks.sarif
```
- ```fetchDepth: 0``` ensures full history is scanned
- findings fail the pipeline
- a SARIF report is always published as a build artifact

**Why it matters**

Secrets committed once remain in Git history forever unless detected.
This prevents accidental credential leaks.

**Common failure & fix**

Pipeline error
```yaml
leaks found: 1
```

Local troubleshooting
```bash
gitleaks detect --config .gitleaks.toml
```

If the secret is:
- real → remove it and rotate the credential
- fake/test → allowlist the exact file path in .gitleaks.toml

### 4.2. Code Formatting – ruff format
**What it does**

Enforces consistent formatting across the codebase.
Pipeline command:

```bash
ruff format --check .
```
If formatting is incorrect, the pipeline fails.
Local fix

```bash
ruff format .
```
Then commit the changes.

### 4.3. Linting – ruff check
**What it does**
Checks for:
-u nused imports
- import ordering
- modern Python practices
- common bug patterns

Pipeline command:

```bash
ruff check .
```
**Common failure & fix**

Pipeline error

```python
I001 Import block is un-sorted or un-formatted
```
Local auto-fix

```bash
ruff check . --fix
```

Re-run:
```bash
ruff check .
```

### 4.4. Type Checking – mypy
**What it does**

Static type checking for Python code under ```src/.```

Pipeline command:

```bash
mypy --explicit-package-bases src
```

The project uses a src-layout, with src/ treated as the package root.

*Why this matters*

Catches:
- incorrect return types
- invalid attribute access
- unsafe None usage
- API misuse

Common failure & fix
Error
```cpp
Source file found twice under different module names
```
Fix
- Ensure ```__init__.py``` exists in:
```css
src/
src/common/
src/backfill/
src/ingestion/
```
- Use consistent imports:
```python
from src.common.config import settings
```
- Never mix ```common.*``` and ```src.common.*```

Local run
```bash
mypy --explicit-package-bases src
```

### 4.5. Tests & Coverage – pytest
**What it does**
Runs unit tests and enforces a minimum coverage threshold.

Pipeline command:
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=40
```
**Why it matters**
- Prevents untested code from accumulating
- Makes refactoring safer

**Common failure & fix**
Coverage failure

```csharp
Coverage failure: total coverage is 32%, minimum required is 40%
```
Local run
```bash
pytest --cov=src --cov-report=term-missing
```
Add tests or lower the threshold temporarily (not recommended long-term).

### 4.6. Dependency Security – pip-audit
**What it does**
Scans requirements.txt for known vulnerabilities (CVEs).
Pipeline command:

```bash
pip-audit -r requirements.txt
```

**Why it matters**
Third-party libraries are a common attack vector.

**Common failure & fix**
Pipeline error
```css
Found known vulnerability in package X
```

Local investigation
```bash
pip-audit -r requirements.txt
```
Fix by:
- upgrading the dependency
- pinning a safe version
- documenting the risk if unavoidable

### 4.7. Docker Build Validation
**What it does**

Ensures the Docker image builds successfully.

Pipeline command:
```bash
docker build -t tradingbot:<build-id> .
```
**Why it matters**
Catches:
- missing files
- broken COPY instructions
- dependency mismatches

## 5. Local Development Workflow (Recommended)
Before pushing code:
```bash
ruff format .
ruff check . --fix
mypy --explicit-package-bases src
pytest --cov=src
pip-audit -r requirements.txt
```
This mirrors CI and prevents surprise failures.

## 6. Summary
This CI pipeline enforces:
- 🔐 Security (gitleaks, pip-audit)
- 🎨 Consistency (ruff format)
- 🧹 Code quality (ruff check)
- 🧠 Correctness (mypy)
- 🧪 Reliability (pytest + coverage)
- 🐳 Deployability (Docker build)

The result is a production-grade CI setup suitable for financial and trading systems.
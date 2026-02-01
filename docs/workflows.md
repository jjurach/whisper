# Project Workflows

This document describes development workflows specific to live-whisper.

## Core Agent Workflow

All AI agents working on this project must follow the **A-E workflow** defined in [AGENTS.md](../AGENTS.md):

- **A: Analyze** - Understand the request and declare intent
- **B: Build** - Create project plan
- **C: Code** - Implement the plan
- **D: Document** - Update documentation
- **E: Evaluate** - Verify against Definition of Done

## Service Management Workflow

The primary way to interact with the live-whisper system is as a background service.

### Commands
```bash
# Start the service
./scripts/runner.sh start

# Stop the service
./scripts/runner.sh stop

# Restart the service
./scripts/runner.sh restart

# Check the status
./scripts/runner.sh status
```

### Logs
Diagnostics and transcription results are logged to `whisper.log` in the project root.
```bash
tail -f whisper.log
```

## Development Workflow

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .[dev]
pre-commit install
```

### 2. Testing
Run the full test suite using `pytest`:
```bash
pytest
```

### 3. Code Quality
The project uses `ruff` for linting and formatting. These are run automatically on commit, but can be run manually:
```bash
ruff check .
ruff format .
```

### 4. Direct Execution for Debugging
Run the script in the foreground to see real-time output and diagnostics:
```bash
python -m live_whisper.live_dictation --model tiny.en --timeout 60
```

## See Also

- [AGENTS.md](../AGENTS.md) - Core A-E workflow
- [Definition of Done](definition-of-done.md) - Quality checklist
- [Architecture](architecture.md) - System design
- [Implementation Reference](implementation-reference.md) - Code patterns

---
Last Updated: 2026-02-01
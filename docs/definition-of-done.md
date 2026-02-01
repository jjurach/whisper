# Definition of Done - live-whisper

**Referenced from:** [AGENTS.md](../AGENTS.md)

This document defines the "Done" criteria for live-whisper. It extends the universal Agent Kernel Definition of Done with project-specific requirements.

## Agent Kernel Definition of Done

This project follows the Agent Kernel Definition of Done. **You MUST review these documents first:**

### Universal Requirements

See **[Universal Definition of Done](system-prompts/principles/definition-of-done.md)** for:
- Plan vs Reality Protocol
- Verification as Data
- Codebase State Integrity
- Agent Handoff
- Status tracking in project plans
- dev_notes/ change documentation requirements

### Python Requirements

See **[Python Definition of Done](system-prompts/languages/python/definition-of-done.md)** for:
- Python environment & dependencies (pyproject.toml, ruff)
- Testing requirements (pytest)
- Code quality standards
- File organization

## Project-Specific Extensions

The following requirements are specific to live-whisper and extend the Agent Kernel DoD:

### 1. Audio and Model Safety

**Mandatory Checks:**
- [ ] No audio stream leaks (verified by running service multiple times).
- [ ] Model downloads are handled gracefully (no timeout during first load).
- [ ] `INPUT_DEVICE_INDEX` is verified for the target system.

### 2. Service Reliability

**Mandatory Checks:**
- [ ] `scripts/runner.sh` correctly identifies the process PID.
- [ ] `whisper.log` contains clear timestamps and diagnostic headers.
- [ ] Keyboard listener terminates cleanly on `ESC`.

## Pre-Commit Checklist

Before committing, verify:

**Code Quality:**
- [ ] Ruff formatting applied: `ruff format .`
- [ ] Ruff linting passes: `ruff check .`
- [ ] Type hints present for new functions.

**Testing:**
- [ ] All unit tests pass: `pytest`
- [ ] Integration test (manual or automated) confirms PTT still works.

**Documentation:**
- [ ] README updated if CLI arguments changed.
- [ ] Architecture docs updated for design changes.

**Commit:**
- [ ] Commit message follows project style.
- [ ] Co-Authored-By trailer included if applicable.

## See Also

- [AGENTS.md](../AGENTS.md) - Core A-E workflow
- [Universal DoD](system-prompts/principles/definition-of-done.md) - Agent Kernel universal requirements
- [Python DoD](system-prompts/languages/python/definition-of-done.md) - Agent Kernel language requirements
- [Architecture](architecture.md) - System design

---
Last Updated: 2026-02-01
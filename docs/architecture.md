# System Architecture

This document describes the architecture of live-whisper.

## High-Level Architecture

live-whisper is a real-time voice dictation tool that follows a pipe-and-filter architecture for processing audio data into text injection.

### Audio Processing Pipeline

1.  **Input Trigger (Keyboard Listener):** Uses `pynput` to monitor for the "Right Control" key press/release.
2.  **Audio Capture (PyAudio):** When the key is held, `pyaudio` captures audio from the default input device.
3.  **Silence/Voice Activity Detection:** The system monitors audio levels to detect when the user is speaking.
4.  **Transcription (Whisper):** Upon key release, the captured audio buffer is passed to the OpenAI Whisper model.
5.  **Punctuation Processing:** Spoken commands (e.g., "period", "new line") are transformed into their respective characters/actions.
6.  **Text Injection (Keyboard Controller):** The final text is injected into the active application using `pynput` to simulate keyboard input.

## Component Overview

-   **`src/live_whisper/live_dictation.py`:** The main entry point. Orchestrates audio capture, model interaction, and keyboard simulation.
-   **`src/live_whisper/transcribe_file.py`:** Utility for batch transcribing existing audio files.
-   **`scripts/runner.sh`:** Service management script (start, stop, status, restart).
-   **`scripts/setup_service.sh` / `setup_autostart.sh`:** Installation scripts for system integration.

## Project Structure

```
live-whisper/
├── AGENTS.md               # Agent instructions
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # Project overview
├── scripts/                # Service management scripts
│   ├── runner.sh
│   ├── setup_autostart.sh
│   └── setup_service.sh
├── src/                    # Source code
│   └── live_whisper/
│       ├── __init__.py
│       ├── live_dictation.py
│       └── transcribe_file.py
├── tests/                  # Test suite
│   ├── test_keyword_replacement.py
│   └── test_live.py
└── docs/                   # Documentation
    ├── architecture.md
    ├── definition-of-done.md
    ├── implementation-reference.md
    ├── templates.md
    ├── workflows.md
    └── system-prompts/      # Agent Kernel
```

## Technology Stack

-   **Language:** Python 3.8+
-   **ML Model:** OpenAI Whisper
-   **Audio I/O:** PyAudio (PortAudio)
-   **Keyboard Control:** pynput
-   **Formatting/Linting:** Ruff
-   **Testing:** pytest

## Agent Kernel Integration

This architecture extends the Agent Kernel reference architecture. See:

- [Agent Kernel Reference Architecture](system-prompts/reference-architecture.md)

## See Also

- [AGENTS.md](../AGENTS.md) - Core workflow
- [Definition of Done](definition-of-done.md) - Quality standards
- [Implementation Reference](implementation-reference.md) - Implementation patterns
- [Workflows](workflows.md) - Development workflows

---
Last Updated: 2026-02-01

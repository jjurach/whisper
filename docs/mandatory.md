# Mandatory Project Guidelines - live-whisper

This document contains mandatory guidelines and rules for the live-whisper project.

## Project Overview

live-whisper is a real-time voice dictation tool. It must be robust, low-latency, and safe to run as a background service.

## Critical Rules

1.  **Audio Device Safety:** Always check for audio device availability before attempting to open a stream.
2.  **Thread Safety:** The keyboard listener and audio capture run in separate threads. Ensure global state access is thread-safe.
3.  **No Blocking in Callbacks:** The PyAudio callback MUST remain non-blocking. Heavy processing (like Whisper transcription) must happen outside the callback.
4.  **Resource Cleanup:** Always use `try...finally` blocks to ensure PyAudio streams and PortAudio instances are terminated correctly.
5.  **Logging:** Use `print(..., flush=True)` or proper logging for all diagnostic output to ensure it appears in `whisper.log` immediately.

## Prohibited Actions

-   **DO NOT** hardcode `INPUT_DEVICE_INDEX` in the source code; it should be configurable.
-   **DO NOT** use large Whisper models by default (e.g., `large-v3`) as they may cause unacceptable latency for real-time use.
-   **DO NOT** modify files in `docs/system-prompts/`.

## When to Stop and Ask for Help

-   If you encounter hardware-specific audio issues (e.g., "ALSA lib... errors") that you cannot resolve.
-   If the push-to-talk mechanism fails to capture key events on a specific platform.
-   If transcription latency consistently exceeds 5 seconds for short phrases.

## See Also

- [AGENTS.md](../AGENTS.md) - Core workflow
- [Architecture](architecture.md) - System design
- [Definition of Done](definition-of-done.md) - Quality standards

---
Last Updated: 2026-02-01

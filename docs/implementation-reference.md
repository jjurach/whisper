# Implementation Reference

This document provides practical implementation patterns and reference implementations for live-whisper.

## Key Patterns

### Push-to-Talk (PTT) Mechanism

The project uses `pynput` for non-blocking keyboard listening to implement PTT.

**Pattern:**
1.  **Listener:** A `pynput.keyboard.Listener` runs in the background.
2.  **`on_press`:** Sets `is_recording = True` and records the start time.
3.  **`on_release`:** Sets `is_recording = False`, stops audio capture, and triggers transcription.

**Reference:** `src/live_whisper/live_dictation.py` (`on_press`, `on_release`, `stop_recording_and_process`)

### Keyword Punctuation Replacement

Spoken commands are replaced with actual punctuation marks using regular expressions to ensure word-boundary matching and case-insensitivity.

**Pattern:**
```python
def process_text(text):
    replacements = {
        "question mark": "?",
        "period": ".",
        # ...
    }
    for keyword, punctuation in replacements.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        text = re.sub(pattern, punctuation, text, flags=re.IGNORECASE)
    return text
```

**Cleanup Regexes:**
- Remove space before terminal punctuation: `re.sub(r'([^ ]) ([.,!?])', r'\1\2', text)`
- Remove spaces around newlines: `re.sub(r' *\n', '\n', text)`

### Audio Resampling

Whisper requires audio at 16,000 Hz. If the input device uses a different rate, the audio must be resampled.

**Pattern:**
```python
if RATE != 16000:
    num_samples = round(len(audio_data) * 16000 / RATE)
    audio_data = resample(audio_data, num_samples)
```

## Testing Patterns

### Mocking Whisper

To test the pipeline without loading the full model, mock the `whisper` instance.

**Reference:** `tests/test_keyword_replacement.py` (if it exists, otherwise see `test_live.py`)

### Testing Keyboard Interaction

Tests for keyboard input simulation should ensure that the `Controller` is correctly used.

## Configuration Patterns

### Environment Variables vs CLI Args

Common settings like `WHISPER_MODEL` and `INPUT_DEVICE_INDEX` are configurable via CLI arguments, allowing for easy integration with service managers like systemd or `runner.sh`.

## See Also

- [Architecture](architecture.md) - System design
- [Workflows](workflows.md) - Development workflows
- [Definition of Done](definition-of-done.md) - Quality standards

---
Last Updated: 2026-02-01

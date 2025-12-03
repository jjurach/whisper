# Real-Time Whisper Dictation

This project provides a real-time, push-to-talk voice dictation tool that uses OpenAI's Whisper model to transcribe speech and input it into any application.

## Features

- **Push-to-Talk:** Hold down the **Right Control** key to record, and release to transcribe.
- **Real-Time Transcription:** Uses the Whisper model for fast and accurate speech-to-text.
- **Apple-Standard Punctuation:** Supports natural speech commands like "period", "comma", "question mark" for automatic punctuation insertion.
- **Cross-Application Input:** Simulates keyboard input, allowing you to dictate into any text field, editor, or application.
- **Configurable Models:** Choose from different Whisper models (`tiny.en`, `small.en`, `medium.en`, etc.) to balance speed and accuracy.
- **Robust Background Service:** Includes a `runner.sh` script to manage the process, with `start`, `stop`, `restart`, and `status` commands.
- **Diagnostic Logging:** All output, including detailed diagnostics, is logged to `whisper.log`.

## Setup

1.  **Prerequisites:** Ensure you have Python 3, `pip`, and `portaudio` installed on your system. On Debian/Ubuntu, you can install `portaudio` with:
    ```bash
    sudo apt-get install portaudio19-dev
    ```

2.  **Create Virtual Environment:** It is highly recommended to use a Python virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:** Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary way to run this tool is as a background service using the provided `runner.sh` script.

### Managing the Service

- **Start:** `bash /home/phaedrus/AiSpace/whisper/runner.sh start`
- **Stop:** `bash /home/phaedrus/AiSpace/whisper/runner.sh stop`
- **Restart:** `bash /home/phaedrus/AiSpace/whisper/runner.sh restart`
- **Status:** `bash /home/phaedrus/AiSpace/whisper/runner.sh status`

### Running in the Foreground

You can also run the script directly in the foreground for debugging purposes.

```bash
# Example with the 'small.en' model and a 60-second timeout
python live_dictation.py --model small.en --timeout 60
```

#### Command-Line Arguments:

- `--model`: Specify the Whisper model to use (e.g., `tiny.en`, `base.en`, `small.en`). Defaults to `tiny.en`.
- `--timeout`: Automatically exit the script after a specified number of seconds.

### How to Dictate

1.  Start the service using `runner.sh start`.
2.  Click into any text field or application.
3.  Press and **hold** the **Right Control** key.
4.  Speak your phrase, using punctuation commands when needed.
5.  **Release** the **Right Control** key.
6.  The transcribed text will be typed out, followed by a space.

### Punctuation Commands

You can include natural punctuation commands in your speech, following Apple's dictation standards:

- **Basic punctuation:** `period`, `comma`, `question mark`, `exclamation point`
- **Symbols:** `dollar sign`, `hashtag`
- **Quotes:** `open quote` ... `close quote`
- **Parentheses:** `open parenthesis` ... `close parenthesis`
- **Formatting:** `new paragraph`, `new line`
- **Other:** `colon`, `semicolon`

**Examples:**
- "Hello world period How are you question mark" → "Hello world. How are you?"
- "She said open quote hello close quote" → "She said "hello""
- "Cost is fifty dollar sign" → "Cost is $50"

## Development and Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [pre-commit](https://pre-commit.com/) hooks to ensure code quality and consistency.

### Setup Development Environment

1.  **Install Development Dependencies:**
    With your virtual environment active, install the development tools specified in `pyproject.toml`:
    ```bash
    pip install .[dev]
    ```

2.  **Install Pre-Commit Hooks:**
    This command sets up Git hooks to automatically run Ruff checks before every commit:
    ```bash
    pre-commit install
    ```

### Usage

-   Ruff will automatically check and format your code on `git commit`. If changes are made, you'll need to `git add` the formatted files and `git commit` again.
-   You can also manually run Ruff:
    -   **Format:** `ruff format .`
    -   **Lint:** `ruff check .`

## Files

- `live_dictation.py`: The main application script.
- `runner.sh`: Service management script for running the application in the background.
- `requirements.txt`: A list of Python dependencies.
- `whisper.log`: Log file where all output and diagnostics are stored.
- `test_live_dictation.py`: Unit tests for the project.
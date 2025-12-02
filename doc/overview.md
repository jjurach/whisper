# Real-Time Whisper Dictation

A push-to-talk voice dictation tool that uses OpenAI's Whisper model to transcribe speech and input it into any application in real-time.

## Purpose

This tool enables hands-free text input through voice dictation, allowing users to speak naturally and have their words transcribed and typed into any application or text field.

## Key Features

- **Push-to-Talk Interface**: Hold Right Control key to record, release to transcribe
- **Real-Time Transcription**: Uses Whisper for fast, accurate speech-to-text conversion
- **Cross-Application Support**: Simulates keyboard input to work with any application
- **Configurable Models**: Choose Whisper model size for speed vs. accuracy trade-offs
- **Background Service**: Robust service management with start/stop/restart/status commands
- **Comprehensive Logging**: All output and diagnostics logged to `whisper.log`

## Architecture

### Components:
- **live_dictation.py**: Main application handling audio capture and transcription
- **transcribe_file.py**: Command-line tool for transcribing audio files
- **Service scripts**: Background process management (runner.sh, setup scripts)

### Audio Pipeline:
1. **Audio Capture**: PyAudio captures system audio when push-to-talk activated
2. **Speech Detection**: Monitors for voice activity and silence
3. **Transcription**: Whisper model processes audio to text
4. **Text Injection**: Simulates keyboard input to insert transcribed text

## Usage

### Service Management
```bash
# Start background service
./scripts/runner.sh start

# Check status
./scripts/runner.sh status

# Stop service
./scripts/runner.sh stop
```

### Dictation Workflow
1. Start service: `./scripts/runner.sh start`
2. Focus target application/text field
3. Hold Right Control key while speaking
4. Release key to inject transcribed text

### Direct Execution
```bash
# Run in foreground with specific model
python -m whisper.live_dictation --model small.en --timeout 300
```

## Supported Models

- `tiny.en`: Fastest, least accurate
- `base.en`: Good balance of speed and accuracy
- `small.en`: Better accuracy, slower
- `medium.en`: High accuracy, slower still
- `large`: Best accuracy, slowest

## Dependencies

- **Core**: openai-whisper, pyaudio, numpy, torch
- **Audio**: portaudio19-dev (system package)
- **Development**: ruff, pre-commit

## Configuration

- **Audio Device**: Automatically detects default input device
- **Model Selection**: Configurable via command line or environment
- **Timeouts**: Automatic exit after specified inactivity periods
- **Logging**: Comprehensive diagnostics to whisper.log
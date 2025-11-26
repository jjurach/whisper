import argparse
import argparse
import pyaudio
import numpy as np
import time
import sys
import threading
import wave
from pprint import pprint
from pynput.keyboard import Key, Listener, Controller
from scipy.signal import resample

# --- CONFIGURATION ---
WHISPER_MODEL = "small.en"  # Choose a fast, small model for real-time
CHUNK = 4096  # Audio buffer size
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Microphone is mono
RATE = 48000  # Your microphone's native sample rate
RECORD_SECONDS = 5  # Maximum length of a single recording snippet

# --- PYNPUT CONFIG ---
keyboard = Controller()
TRIGGER_KEY = Key.ctrl_r  # Right Control for Push-to-Talk
STOP_KEY = Key.esc  # Escape key to quit the script

# --- PYAUDIO CONFIG (MUST BE SET CORRECTLY) ---
# **YOU MUST FIND THIS INDEX:** Run the discovery script below first.
INPUT_DEVICE_INDEX = 3  # Your USB Condenser Microphone is at index 3


# --- GLOBAL STATE ---
is_recording = False
audio_frames = []
p = None
stream = None
whisper_instance = None  # Will be loaded dynamically
record_start_time = 0  # To track key press duration

# --- FUNCTIONS ---


def start_recording():
    global is_recording, audio_frames
    if not is_recording:
        print("\n[REC] Started recording...")
        is_recording = True
        audio_frames = []


def save_audio_to_wav(audio_buffer, channels, sample_width, rate):
    """Saves the given audio buffer to a temporary .wav file."""
    try:
        filename = f"/tmp/recording_{time.strftime('%Y%m%d_%H%M%S')}.wav"
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(audio_buffer)
        print(f"Saved recorded audio to: {filename}", flush=True)
        return filename
    except Exception as e:
        print(f"Error saving .wav file: {e}", flush=True)
        return None


def stop_recording_and_process():
    """Stops a recording, processes the audio, and types the result."""
    global is_recording, stream, record_start_time
    if is_recording:
        key_press_duration = time.time() - record_start_time
        print(f"\n--- DIAGNOSTICS ---", flush=True)
        print(
            f"Control key held down for: {key_press_duration:.2f} seconds", flush=True
        )

        is_recording = False
        print("[REC] Recording finished. Processing...", flush=True)

        if not audio_frames:
            print("[WHISPER] No audio captured.", flush=True)
            print("--- END DIAGNOSTICS ---", flush=True)
            return False

        # --- Refactored Pipeline ---

        # 1. Join and log audio data
        raw_audio_buffer = b"".join(audio_frames)
        recorded_duration = len(raw_audio_buffer) / (
            RATE * p.get_sample_size(FORMAT) * CHANNELS
        )
        print(
            f"Captured {len(audio_frames)} frames, totaling {recorded_duration:.2f}s.",
            flush=True,
        )

        # 2. Save audio to a .wav file
        # save_audio_to_wav(
        #     raw_audio_buffer,
        #     CHANNELS,
        #     p.get_sample_size(FORMAT),
        #     RATE)

        # 3. Convert buffer to numpy array for processing
        audio_data = (
            np.frombuffer(raw_audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0
        )

        # 4. Resample for Whisper
        if RATE != 16000:
            num_samples = round(len(audio_data) * 16000 / RATE)
            audio_data = resample(audio_data, num_samples)
            print(
                f"Resampled audio to {len(audio_data)} samples for Whisper.", flush=True
            )

        # 5. Transcribe with Whisper
        result = transcribe_audio(audio_data)
        transcribed_text = result["text"].strip()

        # 6. (MOCK) Process text with a secondary LLM
        final_text = process_text_with_llm(transcribed_text)
        print(f"Final text to be typed: '{final_text}'", flush=True)

        # 7. Type the final text
        if final_text:
            print("Typing final text...", flush=True)
            keyboard.type(final_text + " ")
        else:
            print("No final text, nothing to type.", flush=True)

        print("--- END DIAGNOSTICS ---", flush=True)
        return True
    return False


# This callback function is called by PyAudio for each audio chunk
def pyaudio_callback(in_data, frame_count, time_info, status):
    if status:
        print(f"[PyAudio Callback Status] Flags: {status}", file=sys.stderr)
    global audio_frames, is_recording
    if is_recording:
        audio_frames.append(in_data)
    return (in_data, pyaudio.paContinue)


def transcribe_audio(audio_data):
    """Transcribes the given audio data using the loaded Whisper model."""
    print("Transcribing with Whisper...", flush=True)
    result = whisper_instance.transcribe(audio_data, fp16=False)
    print("--- Full Whisper Response ---", flush=True)
    pprint(result)
    print("-----------------------------", flush=True)
    return result


def process_text_with_llm(text):
    """
    (MOCK) Processes the transcribed text with a secondary LLM.
    This is a placeholder for future functionality like summarization,
    command extraction, or grammar correction.
    """
    print(f"Processing text '{text}' with secondary LLM (mock)...", flush=True)
    # For now, just append "(processed)" to demonstrate the pipeline
    processed_text = f"{text} (processed)"
    return processed_text


def on_press(key):
    global record_start_time
    # Start recording only when the trigger key is PRESSED
    if key == TRIGGER_KEY:
        # Capture start time only on the initial press
        if not is_recording:
            record_start_time = time.time()
        start_recording()

    # Quit program on ESCAPE
    if key == STOP_KEY:
        # In callback mode, we need to explicitly stop the listener
        return False


def on_release(key):
    # Stop recording and process transcription only when the trigger key is RELEASED
    if key == TRIGGER_KEY:
        stop_recording_and_process()


# --- MAIN EXECUTION ---


def main():
    global p, stream, whisper_instance, INPUT_DEVICE_INDEX

    parser = argparse.ArgumentParser(
        description="A real-time voice dictation tool using Whisper."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="Automatically exit after a specified number of seconds.",
    )
    parser.add_argument(
        "--model",
        default=WHISPER_MODEL,
        help=f"The Whisper model to use (default: {WHISPER_MODEL}).",
    )
    args = parser.parse_args()

    print("Starting Whisper Dictation System...", flush=True)

    # 1. Initialize PyAudio and Whisper
    p = pyaudio.PyAudio()

    stream = None  # Initialize stream to None
    try:
        from whisper import load_model

        print(f"Loading Whisper model: {args.model}...")
        whisper_instance = load_model(args.model)

        # Open the audio stream in callback mode
        print("Initializing audio stream in callback mode...")
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=INPUT_DEVICE_INDEX,
            stream_callback=pyaudio_callback,
            start=False,
        )  # Open stream in 'stopped' state
        print("Audio stream initialized.", flush=True)

    except Exception as e:
        print(f"Error during initialization: {e}", flush=True)
        if p:
            p.terminate()
        sys.exit(1)

    # 2. Start the Listener Loop
    print("-" * 40, flush=True)
    print(f"Dictation Ready. Press and HOLD **Right Control** to record.", flush=True)
    print("Release Right Control to transcribe and type.", flush=True)
    print(f"Press **ESCAPE** to quit.", flush=True)
    print("-" * 40, flush=True)

    # The main logic is wrapped in a try block to ensure cleanup happens
    try:
        # --- INTERACTIVE MODE ---
        print("-" * 40, flush=True)
        print(
            f"Dictation Ready. Press and HOLD **Right Control** to record.", flush=True
        )
        print("Release Right Control to transcribe and type.", flush=True)
        print(f"Press **ESCAPE** to quit.", flush=True)
        if args.timeout:
            print(
                f"Script will automatically exit after {args.timeout} seconds.",
                flush=True,
            )
        print("-" * 40, flush=True)

        with Listener(on_press=on_press, on_release=on_release) as listener:
            # If a timeout is set, start a timer to stop the listener
            if args.timeout:
                timer = threading.Timer(args.timeout, listener.stop)
                timer.daemon = True
                timer.start()

            stream.start_stream()  # Start the stream now that we are ready
            print("Audio stream started. Ready for input.", flush=True)

            listener.join()

    finally:
        # Clean up resources that were initialized before the try block
        print("Cleaning up resources...", flush=True)
        if stream:
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()
        print("\nDictation system terminated.", flush=True)


if __name__ == "__main__":
    main()

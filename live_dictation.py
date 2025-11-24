import argparse
import argparse
import pyaudio
import numpy as np
import time
import sys
import threading
from pynput.keyboard import Key, Listener, Controller
from scipy.signal import resample

# --- CONFIGURATION ---
WHISPER_MODEL = "tiny.en"  # Choose a fast, small model for real-time
CHUNK = 2048               # Audio buffer size
FORMAT = pyaudio.paInt16   # Audio format
CHANNELS = 1               # Microphone is mono
RATE = 44100               # Sample rate required by Whisper
RECORD_SECONDS = 5         # Maximum length of a single recording snippet

# --- PYNPUT CONFIG ---
keyboard = Controller()
TRIGGER_KEY = Key.ctrl_r   # Right Control for Push-to-Talk
STOP_KEY = Key.esc         # Escape key to quit the script

# --- PYAUDIO CONFIG (MUST BE SET CORRECTLY) ---
# **YOU MUST FIND THIS INDEX:** Run the discovery script below first.
INPUT_DEVICE_INDEX = 1  # Placeholder: Update with your AU-A04's index! 


# --- GLOBAL STATE ---
is_recording = False
audio_frames = []
p = None
stream = None
whisper_instance = None # Will be loaded dynamically

# --- FUNCTIONS ---

def start_recording():
    global is_recording, audio_frames
    if not is_recording:
        print("\n[REC] Started recording...")
        is_recording = True
        audio_frames = []


def stop_recording_and_process():
    global is_recording, stream
    if is_recording:
        is_recording = False
        print("[REC] Recording finished. Transcribing...")

        # 2. Process Audio Frames
        if audio_frames:
            # Convert audio frames to a numpy array (Whisper input format)
            audio_data = np.frombuffer(b''.join(audio_frames), dtype=np.int16).astype(np.float32) / 32768.0

            # Resample audio to 16kHz for Whisper
            if RATE != 16000:
                num_samples = round(len(audio_data) * 16000 / RATE)
                audio_data = resample(audio_data, num_samples)
            
            # 3. Transcribe with Whisper
            result = whisper_instance.transcribe(audio_data, fp16=False)
            transcribed_text = result['text'].strip()
            
            print(f"[WHISPER] Text: {transcribed_text}")
            
            # 4. Input Text via Pynput
            if transcribed_text:
                keyboard.type(transcribed_text + " ") # Add a space for clean separation
            
        else:
            print("[WHISPER] No audio captured.")
        
        return True # Processed successfully
    return False # Not recording

# This callback function is called by PyAudio for each audio chunk
def pyaudio_callback(in_data, frame_count, time_info, status):
    global audio_frames, is_recording
    if is_recording:
        audio_frames.append(in_data)
    return (in_data, pyaudio.paContinue)

def on_press(key):
    # Start recording only when the trigger key is PRESSED
    if key == TRIGGER_KEY:
        start_recording()
    
    # Quit program on ESCAPE
    if key == STOP_KEY:
        return False

def on_release(key):
    # Stop recording and process transcription only when the trigger key is RELEASED
    if key == TRIGGER_KEY:
        stop_recording_and_process()

# --- MAIN EXECUTION ---

# --- A. Device Index Discovery (Temporary) ---
def discover_device_index():
    print("--- PyAudio Device Discovery ---")
    p_temp = pyaudio.PyAudio()
    info = p_temp.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    found_mic_index = -1
    for i in range(0, numdevices):
        dev_info = p_temp.get_device_info_by_host_api_device_index(0, i)
        print(f"Device {i}: {dev_info.get('name')} (Input Channels: {dev_info.get('maxInputChannels')})")
        if "Condenser Microphone" in dev_info.get('name') and dev_info.get('maxInputChannels') > 0:
            found_mic_index = i
            print(f"--> Found AU-A04 at index: {found_mic_index}")
    
    p_temp.terminate()
    return found_mic_index

def main():
    global p, stream, whisper_instance, INPUT_DEVICE_INDEX

    parser = argparse.ArgumentParser(description="A real-time voice dictation tool using Whisper.")
    parser.add_argument("--timeout", type=int, help="Automatically exit after a specified number of seconds.")
    parser.add_argument("--model", default=WHISPER_MODEL, help=f"The Whisper model to use (default: {WHISPER_MODEL}).")
    args = parser.parse_args()

    # 0. Discovery and Index Check
    print("Starting Whisper Dictation System...")
    discovered_index = discover_device_index()
    
    if discovered_index != -1:
        INPUT_DEVICE_INDEX = discovered_index
    elif INPUT_DEVICE_INDEX == 1:
        print("\nWARNING: Please manually verify INPUT_DEVICE_INDEX is correct if discovery failed.")
    
    
    # 1. Initialize PyAudio and Whisper
    p = pyaudio.PyAudio()
    stream = None  # Initialize stream to None
    try:
        from whisper import load_model
        print(f"Loading Whisper model: {args.model}...")
        whisper_instance = load_model(args.model)

        # Open the audio stream in callback mode
        print("Initializing audio stream in callback mode...")
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=INPUT_DEVICE_INDEX,
                        stream_callback=pyaudio_callback)
        print("Audio stream initialized.")

    except Exception as e:
        print(f"Error during initialization: {e}")
        if p:
            p.terminate()
        sys.exit(1)

    
    # 2. Start the Listener Loop
    print("-" * 40)
    print(f"Dictation Ready. Press and HOLD **Right Control** to record.")
    print("Release Right Control to transcribe and type.")
    print(f"Press **ESCAPE** to quit.")
    print("-" * 40)

    # The main logic is wrapped in a try block to ensure cleanup happens
    try:
        # --- INTERACTIVE MODE ---
        print("-" * 40)
        print(f"Dictation Ready. Press and HOLD **Right Control** to record.")
        print("Release Right Control to transcribe and type.")
        print(f"Press **ESCAPE** to quit.")
        if args.timeout:
            print(f"Script will automatically exit after {args.timeout} seconds.")
        print("-" * 40)

        with Listener(on_press=on_press, on_release=on_release) as listener:
            # If a timeout is set, start a timer to stop the listener
            if args.timeout:
                timer = threading.Timer(args.timeout, listener.stop)
                timer.daemon = True
                timer.start()

            listener.join()

    finally:
        # Clean up resources that were initialized before the try block
        print("Cleaning up resources...")
        if stream:
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()
        print("\nDictation system terminated.")

if __name__ == "__main__":
    main()

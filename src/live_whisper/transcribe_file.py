#!/usr/bin/env python
import argparse
import sys

import numpy as np
import whisper
from scipy.io import wavfile
from scipy.signal import resample


def main():
    """
    Transcribes a .wav file using the specified Whisper model and outputs the
    result to standard output.
    """
    parser = argparse.ArgumentParser(
        description="Transcribe a .wav file using Whisper and print to stdout."
    )
    parser.add_argument(
        "input_file", type=str, help="Path to the input .wav file to be transcribed."
    )
    parser.add_argument(
        "--model",
        default="small.en",
        help=(
            "The Whisper model to use (e.g., tiny.en, base.en, small.en). "
            "Default: small.en"
        ),
    )
    args = parser.parse_args()

    try:
        # 1. Load the Whisper model
        print(f"Loading Whisper model: {args.model}...", file=sys.stderr)
        model = whisper.load_model(args.model)

        # 2. Read the audio file
        print(f"Reading audio file: {args.input_file}", file=sys.stderr)
        samplerate, data = wavfile.read(args.input_file)
        print(f"Original audio specs: {samplerate} Hz, {data.dtype}", file=sys.stderr)

        # 3. Prepare audio data for Whisper
        # Convert to mono if it's stereo
        if len(data.shape) > 1 and data.shape[1] > 1:
            print("Audio is stereo, converting to mono.", file=sys.stderr)
            data = data.mean(axis=1)

        # Get the original data type to normalize correctly
        original_dtype = data.dtype

        # Normalize to float32
        audio_data = data.astype(np.float32)

        # Use the correct maximum for the original dtype
        if np.issubdtype(original_dtype, np.integer):
            max_val = np.iinfo(original_dtype).max
            print(
                f"Normalizing audio based on original dtype '{original_dtype}' "
                f"with max value {max_val}.",
                file=sys.stderr,
            )
            audio_data /= max_val

        # Ensure data is in the range [-1.0, 1.0]
        audio_data = np.clip(audio_data, -1.0, 1.0)

        # 4. Resample to 16kHz if necessary
        if samplerate != 16000:
            print(f"Resampling from {samplerate} Hz to 16000 Hz...", file=sys.stderr)
            num_samples = round(len(audio_data) * 16000 / samplerate)
            audio_data = resample(audio_data, num_samples)

            # Re-clamp after resampling, as it can introduce values outside the range
            audio_data = np.clip(audio_data, -1.0, 1.0)
            print(
                f"Resampling complete. Final sample count: {len(audio_data)}",
                file=sys.stderr,
            )

        # 5. Transcribe the audio
        print("Transcribing...", file=sys.stderr)
        result = model.transcribe(audio_data, fp16=False)
        transcribed_text = result["text"].strip()

        # 6. Output the final text to stdout
        print(transcribed_text)

    except FileNotFoundError:
        print(f"Error: Input file not found at '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

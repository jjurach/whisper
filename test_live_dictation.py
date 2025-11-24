import unittest
from unittest.mock import patch, MagicMock, call
import numpy as np

# Import the functions and variables from the script to be tested
import live_dictation as ld
from pynput.keyboard import Key

class TestLiveDictation(unittest.TestCase):

    def setUp(self):
        """Set up a clean state before each test."""
        ld.is_recording = False
        ld.audio_frames = []
        
        # Mocking external dependencies
        self.pyaudio_patch = patch('live_dictation.pyaudio')
        self.whisper_patch = patch('live_dictation.whisper_instance')
        self.keyboard_patch = patch('live_dictation.keyboard')
        
        self.mock_pyaudio = self.pyaudio_patch.start()
        self.mock_whisper = self.whisper_patch.start()
        self.mock_keyboard = self.keyboard_patch.start()

    def tearDown(self):
        """Clean up patches after each test."""
        self.pyaudio_patch.stop()
        self.whisper_patch.stop()
        self.keyboard_patch.stop()

    def test_start_recording(self):
        """Verify that start_recording sets the recording flag and clears previous frames."""
        ld.audio_frames = [b'some_old_data']
        ld.start_recording()
        self.assertTrue(ld.is_recording)
        self.assertEqual(ld.audio_frames, [])

    def test_stop_recording_and_process_when_not_recording(self):
        """Verify that processing does not occur if not recording."""
        result = ld.stop_recording_and_process()
        self.assertFalse(result)
        self.mock_whisper.transcribe.assert_not_called()

    def test_stop_recording_and_process_with_no_audio(self):
        """Verify behavior when recording stops with no audio captured."""
        ld.is_recording = True
        result = ld.stop_recording_and_process()
        self.assertTrue(result)
        self.assertFalse(ld.is_recording)
        self.mock_whisper.transcribe.assert_not_called()
        self.mock_keyboard.type.assert_not_called()

    @patch('live_dictation.resample')
    def test_stop_recording_and_process_with_audio(self, mock_resample):
        """Verify audio processing, resampling, transcription, and typing."""
        # 1. Setup
        ld.is_recording = True
        # Simulate raw audio frames (16-bit integers)
        fake_audio_chunk = np.random.randint(-32768, 32767, size=ld.CHUNK, dtype=np.int16)
        ld.audio_frames = [fake_audio_chunk.tobytes()]

        # Mock the transcription result
        self.mock_whisper.transcribe.return_value = {'text': '  hello world  '}
        
        # Mock the resampler to return a predictable output
        mock_resample.return_value = np.zeros(100, dtype=np.float32)

        # 2. Execute
        result = ld.stop_recording_and_process()

        # 3. Assert
        self.assertTrue(result)
        self.assertFalse(ld.is_recording)

        # Check if resampling was called correctly
        self.assertEqual(ld.RATE, 44100) # Ensure original rate requires resampling
        mock_resample.assert_called_once()

        # Check if transcription was called
        self.mock_whisper.transcribe.assert_called_once()
        # Verify the transcribed text is typed correctly (stripped with a space)
        self.mock_keyboard.type.assert_called_once_with("hello world ")

    def test_pyaudio_callback(self):
        """Verify the callback appends audio only when recording."""
        fake_data = b'x01x02'
        
        # Should not append data if not recording
        ld.is_recording = False
        ld.pyaudio_callback(fake_data, 0, 0, 0)
        self.assertEqual(len(ld.audio_frames), 0)

        # Should append data when recording
        ld.is_recording = True
        ld.pyaudio_callback(fake_data, 0, 0, 0)
        self.assertEqual(len(ld.audio_frames), 1)
        self.assertEqual(ld.audio_frames[0], fake_data)

    @patch('live_dictation.start_recording')
    def test_on_press_trigger_key(self, mock_start_recording):
        """Verify that the trigger key starts recording."""
        ld.on_press(ld.TRIGGER_KEY)
        mock_start_recording.assert_called_once()

    def test_on_press_stop_key(self):
        """Verify that the stop key returns False to exit listener."""
        result = ld.on_press(ld.STOP_KEY)
        self.assertFalse(result)

    @patch('live_dictation.stop_recording_and_process')
    def test_on_release_trigger_key(self, mock_stop_recording):
        """Verify that releasing the trigger key stops recording."""
        ld.on_release(ld.TRIGGER_KEY)
        mock_stop_recording.assert_called_once()

    def test_on_release_other_key(self):
        """Verify that releasing other keys does nothing."""
        ld.on_release(Key.shift)
        # No error should be raised, and no functions should be called.
        # This implicitly tests that nothing happens.

if __name__ == '__main__':
    unittest.main()

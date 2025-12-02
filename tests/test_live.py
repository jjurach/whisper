import unittest
from unittest.mock import patch, MagicMock

# We have to be careful about the order of imports and mocks
# Import the script to be tested
import live_dictation


class TestProcessingPipeline(unittest.TestCase):
    @patch("live_dictation.wave.open")
    def test_save_audio_to_wav(self, mock_wave_open):
        """
        Tests that the save_audio_to_wav function calls the wave module
        with the correct parameters.
        """
        # Create a mock wave object
        mock_wf = MagicMock()
        mock_wave_open.return_value.__enter__.return_value = mock_wf

        # Prepare dummy data
        dummy_buffer = b"\x01\x02\x03"
        dummy_channels = 1
        dummy_width = 2
        dummy_rate = 16000

        # Call the function
        filename = live_dictation.save_audio_to_wav(
            dummy_buffer, dummy_channels, dummy_width, dummy_rate
        )

        # Assertions
        self.assertIsNotNone(filename)
        self.assertTrue(filename.startswith("/tmp/recording_"))
        self.assertTrue(filename.endswith(".wav"))

        # Check that wave.open was called correctly
        mock_wave_open.assert_called_once_with(filename, "wb")

        # Check that the wave object's methods were called with correct parameters
        mock_wf.setnchannels.assert_called_once_with(dummy_channels)
        mock_wf.setsampwidth.assert_called_once_with(dummy_width)
        mock_wf.setframerate.assert_called_once_with(dummy_rate)
        mock_wf.writeframes.assert_called_once_with(dummy_buffer)

    def test_process_text_with_llm_mock(self):
        """
        Tests the mock LLM processing function.
        """
        input_text = "hello world"
        expected_output = "hello world (processed)"

        processed_text = live_dictation.process_text_with_llm(input_text)

        self.assertEqual(processed_text, expected_output)

    @patch("live_dictation.whisper_instance")
    def test_transcribe_audio(self, mock_whisper_instance):
        """
        Tests the transcribe_audio function by mocking the whisper model.
        """
        # Configure the mock whisper instance
        mock_whisper_instance.transcribe.return_value = {
            "text": "this is a test",
            "language": "en",
        }

        # Create dummy audio data (not important as the model is mocked)
        dummy_audio_data = b""

        # Call the function
        result = live_dictation.transcribe_audio(dummy_audio_data)

        # Assertions
        mock_whisper_instance.transcribe.assert_called_once_with(
            dummy_audio_data, fp16=False
        )
        self.assertIn("text", result)
        self.assertEqual(result["text"], "this is a test")


if __name__ == "__main__":
    unittest.main()

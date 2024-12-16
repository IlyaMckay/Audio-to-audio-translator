import unittest
from audio_processing_module.audio_processing import AudioToAudio

class TestAudioProcessing(unittest.TestCase):
    def setUp(self):
        self.transcriber = AudioToAudio()

    def test_audio_segmentation(self):
        segments = self.transcriber.audio_segmentation("example_audio.mp3")
        self.assertTrue(len(segments) > 0, "Audio should be segmented into non-zero parts.")

    def test_translation(self):
        result = self.transcriber.translate_text("en", "Hello, world!")
        self.assertEqual(result, "Привет, мир!", "Translation should return correct result.")

if __name__ == "__main__":
    unittest.main()

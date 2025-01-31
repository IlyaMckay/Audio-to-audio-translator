import unittest
from io import BytesIO
from pydub import AudioSegment
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
    
    def test_transcribe_segment(self):
        silent_audio = AudioSegment.silent(duration=1000)
        text, lang = self.transcriber.transcribe_segment(silent_audio)

        if text is None and lang is None:
            self.assertIsNone(text, "Transcription result should be None on failure.")
            self.assertIsNone(lang, "Language code should be None on failure.")
        else:
            self.assertIsInstance(text, str, "Transcription result should be a string.")
            self.assertIsInstance(lang, str, "Language code should be a string.")


    def test_say_it_aloud(self):
        text = "Привет, мир!"
        audio_segment = self.transcriber.say_it_aloud(text)
        
        self.assertIsInstance(audio_segment, AudioSegment, "Synthesized output should be an AudioSegment.")
        self.assertGreater(len(audio_segment.raw_data), 0, "Generated audio should not be empty.")

if __name__ == "__main__":
    unittest.main()

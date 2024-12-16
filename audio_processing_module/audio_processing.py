import os
import re
from io import BytesIO
import assemblyai as aai
from vosk_tts import Model, Synth
from pydub import AudioSegment, silence
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()


class AudioToAudio:
    """
    A class that processes audio files to segment, transcribe, translate, and synthesize them back to audio.

    The class uses silence-based segmentation to split an audio file, transcribes the segments using a transcription service,
    optionally translates text to a target language, and generates audio output for the translated or original text.
    """

    def __init__(self):
        """
        Initialize the AudioToAudio class with configurations for transcription, voice synthesis, and silence handling.

        Attributes:
            aai_config (TranscriptionConfig): Configuration for the transcription API, including punctuation, 
                language detection, and speech model selection.
            vosk_model (Model): Pretrained VOSK model for text-to-speech synthesis.
            silence (AudioSegment): A predefined silent audio segment for padding or separating synthesized outputs.
        """
        aai.settings.api_key = os.getenv('API_KEY')

        self.aai_config = aai.TranscriptionConfig(
            punctuate=True,
            format_text=True,
            language_confidence_threshold=0.8,
            speech_model=aai.SpeechModel.best,
            language_detection=True,
        )

        self.vosk_model = Model(model_name="vosk-model-tts-ru-0.7-multi")

        self.silence = AudioSegment.silent(duration=650)

    def audio_segmentation(self, audio_file) -> list:
        """
        Split an audio file into segments based on silence detection.

        Args:
            audio_file (str): Path to the audio file to be segmented.

        Returns:
            list: A list of `AudioSegment` objects representing the audio segments.
        """

        audio = AudioSegment.from_file(audio_file)
        audio = audio.set_channels(1).set_frame_rate(16000)

        segments = silence.split_on_silence(
            audio, min_silence_len=500, silence_thresh=-40, keep_silence=1200
        )

        return segments

    def transcribe_segment(self, segment_to_transcribe) -> tuple:
        """
        Transcribe an audio segment and detect its language.

        Args:
            segment_to_transcribe (AudioSegment): The audio segment to be transcribed.

        Returns:
            tuple: A tuple containing the transcribed text and the detected language code.
        """

        aai_transcriber = aai.Transcriber(config=self.aai_config)

        audio_bytes = BytesIO()
        segment_to_transcribe.export(audio_bytes, format="wav")
        audio_bytes.seek(0)

        try:
            transcript = aai_transcriber.transcribe(audio_bytes)

        except Exception as e:
            print(f"Transcription error occurred. {e}")

        return transcript.text, transcript.json_response["language_code"]

    def translate_text(self, lang_code: str, text_to_translate: str) -> str:
        """
        Translate text into Russian if the original language is English.

        Args:
            lang_code (str): The language code of the text (e.g., "en" for English).
            text_to_translate (str): The text to translate.

        Returns:
            str: Translated text if the input is in English, otherwise `None`.
        """

        if lang_code != "en" or re.search(r"senh", text_to_translate, re.IGNORECASE):
            return None

        translated_text = GoogleTranslator(source="en", target="ru").translate(
            text_to_translate
        )

        return translated_text

    def say_it_aloud(self, text_to_say_aloud):
        """
        Generate synthesized speech from the provided text.

        Args:
            text_to_say_aloud (str): The text to be synthesized into speech.

        Returns:
            AudioSegment: An `AudioSegment` object representing the synthesized speech.
        """

        synth = Synth(self.vosk_model)
        synth_audio = BytesIO()
        synth.synth(
            text_to_say_aloud,
            oname=synth_audio,
            speaker_id=4,
            speech_rate=0.9
        )
        synth_audio.seek(0)
        audio_segment = AudioSegment.from_file(
            synth_audio,
            format="wav"
        )

        return audio_segment

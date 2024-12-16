from flask import render_template, request, send_file
from pydub import AudioSegment
from io import BytesIO
from audio_processing_module.audio_processing import AudioToAudio
from werkzeug.utils import secure_filename
from app import app


@app.route("/")
def home():
    """Render the homepage with a file upload form."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    """Handle audio file upload, process it, and return a downloadable file."""
    if "audio" not in request.files:
        return "No file uploaded", 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return "No selected file", 400

    original_filename = secure_filename(audio_file.filename)
    output_filename = f"rus_{original_filename}"

    transcriber = AudioToAudio()

    audio_data = audio_file.read()

    final_audio = AudioSegment.empty()

    audio_segments = transcriber.audio_segmentation(BytesIO(audio_data))
    for segment in audio_segments:
        text, lang = transcriber.transcribe_segment(segment)
        if lang == "en":
            translated_segment = transcriber.translate_text(lang, text)
            final_audio += (
                transcriber.say_it_aloud(translated_segment) + transcriber.silence
            )
        else:
            final_audio += segment

    normalized_audio = final_audio.normalize()
    output_audio = BytesIO()
    normalized_audio.export(output_audio, format="mp3")
    output_audio.seek(0)

    return send_file(
        output_audio,
        as_attachment=True,
        download_name=output_filename,
        mimetype="audio/mp3",
    )

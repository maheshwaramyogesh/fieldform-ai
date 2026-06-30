from faster_whisper import WhisperModel
import tempfile

# Load the model only once when the app starts
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8",
)


def transcribe_audio(uploaded_audio):
    """
    Convert Streamlit audio input into text.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_audio.read())
        audio_path = temp_audio.name

    segments, info = model.transcribe(audio_path)

    transcript = " ".join(segment.text.strip() for segment in segments)

    return transcript

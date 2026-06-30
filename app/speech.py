import tempfile

from faster_whisper import WhisperModel

_model = None


def _get_model():
    global _model

    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    return _model


def transcribe_audio(uploaded_audio):
    """
    Convert Streamlit audio input into text.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_audio.read())
        audio_path = temp_audio.name

    segments, _info = _get_model().transcribe(audio_path)

    transcript = " ".join(segment.text.strip() for segment in segments)

    return transcript

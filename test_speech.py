from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("Model loaded!")

audio_file = "sample.wav"

segments, info = model.transcribe(
    audio_file,
    beam_size=5,
    language="en",
    vad_filter=True,
    vad_parameters={
        "min_silence_duration_ms": 500,
    },
)

print("\nDetected language:", info.language)
print("Probability:", info.language_probability)

transcript_parts = []

for segment in segments:
    transcript_parts.append(segment.text.strip())

transcript = " ".join(transcript_parts)
print(segment.text)
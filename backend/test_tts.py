
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

print("Kisan Sunaai - Hindi Voice Test")

client = GnaniTTSClient()

text = "नमस्ते किसान भाई। आपकी शिकायत सफलतापूर्वक सेव हो गई है।"

print("Generating Hindi voice...")

audio = client.synthesize(
    text,
    voice="Nalini",
    model="timbre-v2.5",
    language="hi-IN",
    audio_config=AudioConfig(
        container="wav",
        sample_rate=22050
    )
)

with open("kisan_response.wav", "wb") as file:
    file.write(audio)

print("Voice generated successfully!")
print("Audio saved as kisan_response.wav")

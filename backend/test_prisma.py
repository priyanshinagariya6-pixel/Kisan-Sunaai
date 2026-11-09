from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient

load_dotenv()

client = GnaniSTTClient()

result = client.transcribe(
    "sample.wav",
    language_code="hi-IN",
    model="prisma-v3.0"
)

print("\n===== KISAN SUNAAI =====")
print("Farmer's voice converted into text:")
print(result["transcript"])
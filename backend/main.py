
import json
from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from complaint_analyzer import analyze_complaint

load_dotenv()


def process_farmer_voice():

    print("\n===== KISAN SUNAAI =====")
    print("Processing farmer's voice...")

    # Step 1: Voice to Text using Gnani
    client = GnaniSTTClient()

    result = client.transcribe(
        "sample.wav",
        language_code="hi-IN",
        model="prisma-v3.0"
    )

    transcript = result["transcript"]

    print("\nFarmer's Complaint:")
    print(transcript)

    # Step 2: Analyze complaint using Gemini
    print("\nGemini is analyzing the complaint...")

    complaint = analyze_complaint(transcript)

    print("\n===== FINAL COMPLAINT REPORT =====")
    print(json.dumps(complaint, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    process_farmer_voice()

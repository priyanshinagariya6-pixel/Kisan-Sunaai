
import sys
import os
import json
import uuid
import time
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient, AudioConfig
from transformers import pipeline
from google import genai

from save_complaint import save_complaint


# =====================================
# STEP 1: LOAD API KEYS
# =====================================

load_dotenv()

gnani_key = os.getenv("GNANI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not gnani_key:
    raise ValueError("GNANI_API_KEY missing in .env file")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY missing in .env file")

gemini_client = genai.Client(api_key=gemini_key)
stt_client = GnaniSTTClient()
tts_client = GnaniTTSClient()


# =====================================
# STEP 2: GET AUDIO FILE
# =====================================

audio_file = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"

if not os.path.exists(audio_file):
    raise FileNotFoundError(f"Audio file not found: {audio_file}")

if os.path.getsize(audio_file) == 0:
    raise ValueError("Audio file is empty.")

print("\n===== KISAN SUNAAI =====")
print("Processing farmer's voice complaint...")


# =====================================
# STEP 3: SPEECH TO TEXT
# =====================================

result = stt_client.transcribe(
    audio_file,
    language_code="hi-IN",
    model="prisma-v3.0"
)

complaint = result.get("transcript", "").strip()

if not complaint:
    raise ValueError("No speech detected in the audio.")

print("\nFarmer's Complaint:")
print(complaint)


# =====================================
# STEP 4: CLASSIFY COMPLAINT
# =====================================

print("\nClassifying complaint...")

classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
)

categories = [
    "PM Kisan payment issue",
    "Fertilizer shortage",
    "Crop damage",
    "Government scheme issue",
    "Crop disease or pest problem",
    "Irrigation or water problem",
    "Other farmer problem"
]

prediction = classifier(complaint, categories)

category = prediction["labels"][0]
confidence = round(float(prediction["scores"][0]), 2)

print("\nPredicted Category:", category)
print("Confidence:", confidence)



# =====================================
# STEP 5: GEMINI AI ANALYSIS
# =====================================

print("\nGemini is analyzing the complaint...")

prompt = f"""
You are Kisan Sunaai, an AI farmer support assistant
for farmers in Madhya Pradesh.

Farmer complaint:
{complaint}

Respond in simple Hindi using these headings:

1. समस्या का सारांश
2. शिकायत की श्रेणी
3. संबंधित संभावित विभाग
4. किसान से पूछे जाने वाले जरूरी सवाल
5. किसान के लिए अगले कदम

Do not invent government rules.
Do not claim official submission.
Never ask for full Aadhaar, OTP or password.
"""

analysis_text = (
    "Gemini AI abhi available nahi hai. "
    "कृपया कुछ समय बाद दोबारा प्रयास करें। "
    "फसल की समस्या के लिए स्थानीय कृषि विशेषज्ञ "
    "या कृषि विज्ञान केंद्र से सलाह लें।"
)

try:
    response = gemini_client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if response.text:
        analysis_text = response.text

    print("\nGemini analysis completed!")

except Exception as error:
    print("\nGemini temporarily unavailable:", error)
    print("Using fallback response.")

print("\n===== GEMINI AI ANALYSIS =====")
print(analysis_text)


# =====================================
# STEP 6: CREATE COMPLAINT RECORD
# =====================================

complaint_id = str(uuid.uuid4())[:8]

complaint_record = {
    "complaint_id": complaint_id,
    "complaint": complaint,
    "category": category,
    "confidence": confidence,
    "analysis": analysis_text,
    "date": datetime.now().isoformat(),
    "status": "Draft - Not Submitted"
}


# =====================================
# STEP 7: SAVE COMPLAINT
# =====================================

save_complaint(complaint_record)

print("\nComplaint saved successfully!")


# =====================================
# STEP 8: GENERATE HINDI VOICE RESPONSE
# =====================================

voice_file = None

voice_text = (
    "नमस्ते किसान भाई। "
    "आपकी शिकायत सफलतापूर्वक सेव हो गई है। "
    f"आपकी शिकायत आईडी {complaint_id} है। "
    "ध्यान दें, शिकायत अभी आधिकारिक रूप से दर्ज नहीं हुई है।"
)

print("\nGenerating Hindi voice response...")

try:
    audio = tts_client.synthesize(
        voice_text,
        voice="Nalini",
        model="timbre-v2.5",
        language="hi-IN",
        audio_config=AudioConfig(
            container="wav",
            sample_rate=22050
        )
    )

    voice_file = "kisan_complaint_response.wav"

    with open(voice_file, "wb") as file:
        file.write(audio)

    print("Hindi voice response generated successfully!")

except Exception as error:
    print("TTS temporarily unavailable:", error)


# =====================================
# STEP 9: FINAL RESULT
# =====================================

final_result = {
    "complaint_id": complaint_id,
    "complaint": complaint,
    "category": category,
    "confidence": confidence,
    "analysis": analysis_text,
    "status": "Draft - Not Submitted",
    "voice_file": voice_file
}

print("\n================================")
print("       KISAN SUNAAI RESULT")
print("================================")

print(json.dumps(final_result, ensure_ascii=False, indent=4))

print("\nYour complaint has been saved successfully!")
print("Use this Complaint ID to track your complaint.")

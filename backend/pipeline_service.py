
import os
import uuid
import threading
from datetime import datetime

from dotenv import load_dotenv
from gnani.stt import GnaniSTTClient
from gnani.tts import GnaniTTSClient, AudioConfig
from google import genai

from classifier_service import classify_complaint
from save_complaint import save_complaint

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API clients are created only once
gnani_key = os.getenv("GNANI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

if not gnani_key:
    raise ValueError("GNANI_API_KEY missing in .env")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY missing in .env")

stt_client = GnaniSTTClient()
tts_client = GnaniTTSClient()
gemini_client = genai.Client(api_key=gemini_key)

# Prevent simultaneous writes to complaint storage
complaint_lock = threading.Lock()


def process_complaint(audio_path):

    # 1. Speech to text
    result = stt_client.transcribe(
        audio_path,
        language_code="hi-IN",
        model="prisma-v3.0"
    )

    complaint = result.get("transcript", "").strip()

    if not complaint:
        raise ValueError("No speech detected.")

    # 2. Classify complaint using already-loaded model
    classification = classify_complaint(complaint)

    category = classification["category"]
    confidence = classification["confidence"]

    # 3. Gemini analysis
    prompt = f"""
You are Kisan Sunaai, an AI farmer support assistant
for farmers in Madhya Pradesh.

Farmer complaint:
{complaint}

Respond in simple Hindi with:
1. समस्या का सारांश
2. शिकायत की श्रेणी
3. संभावित कारण
4. किसान से पूछे जाने वाले जरूरी सवाल
5. किसान के अगले कदम

Do not invent government rules.
Do not claim official submission.
Never ask for full Aadhaar, OTP or password.
"""

    analysis_text = (
        "Gemini AI अभी उपलब्ध नहीं है। कृपया कुछ समय बाद दोबारा प्रयास करें।"
    )

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if response.text:
            analysis_text = response.text

    except Exception as error:
        print("Gemini error:", str(error))

    # 4. Create complaint record
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

    # 5. Save complaint
    with complaint_lock:
        save_complaint(complaint_record)

    # 6. Generate Hindi voice response
    voice_file = None

    voice_text = (
        f"नमस्ते किसान भाई। आपकी शिकायत की आईडी {complaint_id} है। "
        "ध्यान दें, शिकायत अभी आधिकारिक रूप से दर्ज नहीं हुई है।"
    )

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

        with open(os.path.join(BASE_DIR, voice_file), "wb") as file:
            file.write(audio)

    except Exception as error:
        print("TTS error:", str(error))

    return {
        "complaint_id": complaint_id,
        "complaint": complaint,
        "category": category,
        "confidence": confidence,
        "analysis": analysis_text,
        "status": "Draft - Not Submitted",
        "voice_file": voice_file
    }

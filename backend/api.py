
import json
import os
import uuid
import threading
import traceback

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool

from pipeline_service import process_complaint


# =====================================
# 1. FASTAPI APPLICATION
# =====================================

app = FastAPI(
    title="Kisan Sunaai API",
    description="AI-powered farmer complaint assistance system",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# 2. FILE PATHS
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "complaints.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Process one complaint at a time
PIPELINE_LOCK = threading.Lock()


def run_pipeline_safely(audio_path):
    with PIPELINE_LOCK:
        return process_complaint(audio_path)


# =====================================
# 3. HOME API
# =====================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Kisan Sunaai API",
        "status": "Running"
    }


# =====================================
# 4. GET ALL COMPLAINTS
# =====================================

@app.get("/complaints")
def get_complaints():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        raise HTTPException(
            status_code=500,
            detail="Unable to read complaint records."
        )


# =====================================
# 5. TRACK COMPLAINT
# =====================================

@app.get("/track/{complaint_id}")
def track_complaint(complaint_id: str):

    if not os.path.exists(DATA_FILE):
        raise HTTPException(
            status_code=404,
            detail="No complaints found."
        )

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            complaints = json.load(file)

        for record in complaints:
            if record.get("complaint_id") == complaint_id:
                return record

        raise HTTPException(
            status_code=404,
            detail="Complaint not found."
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Complaint database is corrupted."
        )


# =====================================
# 6. VOICE COMPLAINT API
# =====================================

@app.post("/voice-complaint")
async def voice_complaint(file: UploadFile = File(...)):

    audio_path = None

    if not file.filename or not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a WAV audio file."
        )

    try:
        audio_data = await file.read()

        if not audio_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty."
            )

        audio_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4()}.wav"
        )

        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)

        # Run blocking AI work outside the async event loop
        complaint_result = await run_in_threadpool(
            run_pipeline_safely,
            audio_path
        )

        return {
            "message": "Complaint processed successfully",
            "complaint": complaint_result
        }

    except HTTPException:
        raise

    except Exception as error:
        print("VOICE COMPLAINT ERROR:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="AI complaint processing failed. Check backend logs."
        )

    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                print("Warning: Temporary audio could not be deleted.")

        await file.close()

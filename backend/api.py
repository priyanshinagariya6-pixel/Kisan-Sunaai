
import json
import os
import subprocess
import sys
import uuid
import traceback

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# =====================================
# 1. FASTAPI APPLICATION
# =====================================

app = FastAPI(
    title="Kisan Sunaai API",
    description="AI-powered farmer complaint assistance system",
    version="1.0"
)

# =====================================
# 2. CORS CONFIGURATION
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# 3. FILE PATHS
# =====================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "complaints.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
PIPELINE_FILE = os.path.join(BASE_DIR, "complaint_pipeline.py")

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =====================================
# 4. HOME API
# =====================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Kisan Sunaai API",
        "status": "Running"
    }


# =====================================
# 5. GET ALL COMPLAINTS
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
# 6. TRACK COMPLAINT
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
# 7. VOICE COMPLAINT API
# =====================================

@app.post("/voice-complaint")
async def voice_complaint(file: UploadFile = File(...)):

    audio_path = None

    # Check filename
    if not file.filename or not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a WAV audio file."
        )

    try:
        # ---------------------------------
        # STEP 1: SAVE UPLOADED AUDIO
        # ---------------------------------

        audio_path = os.path.join(
            UPLOAD_DIR,
            f"{uuid.uuid4()}.wav"
        )

        audio_data = await file.read()

        if not audio_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded audio file is empty."
            )

        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)

        # ---------------------------------
        # STEP 2: CHECK PIPELINE FILE
        # ---------------------------------

        if not os.path.exists(PIPELINE_FILE):
            raise HTTPException(
                status_code=500,
                detail="Complaint pipeline file not found."
            )

        # ---------------------------------
        # STEP 3: RUN AI PIPELINE
        # ---------------------------------

        result = subprocess.run(
            [
                sys.executable,
                PIPELINE_FILE,
                audio_path
            ],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600
        )

        # ---------------------------------
        # STEP 4: CHECK PIPELINE RESULT
        # ---------------------------------

        if result.returncode != 0:

            print("PIPELINE ERROR:")
            print(result.stderr[-4000:])

            raise HTTPException(
                status_code=500,
                detail="AI complaint processing failed. Check backend logs."
            )

        # ---------------------------------
        # STEP 5: READ SAVED COMPLAINTS
        # ---------------------------------

        if not os.path.exists(DATA_FILE):
            raise HTTPException(
                status_code=500,
                detail="Complaint was not saved."
            )

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            complaints = json.load(file)

        if not complaints:
            raise HTTPException(
                status_code=500,
                detail="No complaint record found."
            )

        # ---------------------------------
        # STEP 6: RETURN LATEST COMPLAINT
        # ---------------------------------

        latest_complaint = complaints[-1]

        return {
            "message": "Complaint processed successfully",
            "complaint": latest_complaint,
            "pipeline_output": result.stdout
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Complaint processing timed out. Please try again."
        )

    except HTTPException:
        raise

    except Exception as e:

        print("VOICE COMPLAINT ERROR:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

    finally:

        # ---------------------------------
        # STEP 7: DELETE TEMPORARY AUDIO
        # ---------------------------------

        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except OSError:
                print("Warning: Temporary audio file could not be deleted.")

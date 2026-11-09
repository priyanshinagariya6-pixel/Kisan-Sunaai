
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = genai.Client(api_key=api_key)

complaint = input("Enter farmer complaint: ")

prompt = f"""
You are Kisan Sunaai, a farmer support assistant.

Analyze this farmer complaint:
{complaint}

Respond in simple Hindi with:
1. Problem summary
2. Complaint category
3. Department that may handle it
4. Information still needed from farmer

Do not claim the complaint has been officially submitted.
"""

print("\nGemini is analyzing your complaint...")

for attempt in range(1, 4):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        print("\n===== KISAN SUNAAI ANALYSIS =====")
        print(response.text)
        break

    except Exception as error:
        print(f"\nAttempt {attempt} failed: {error}")

        if attempt < 3:
            print("Retrying after 5 seconds...")
            time.sleep(5)
        else:
            print("\nGemini is currently unavailable.")
            print("Please try again later.")

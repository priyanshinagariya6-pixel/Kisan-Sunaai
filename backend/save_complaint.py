
import json
import os

def save_complaint(record):
    filename = "complaints.json"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            complaints = json.load(file)
    else:
        complaints = []

    complaints.append(record)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(complaints, file, ensure_ascii=False, indent=4)

    print("Complaint saved successfully!")

print("Kisan Sunaai storage system ready!")


import json

complaint_id = input("Enter Complaint ID: ")

with open("complaints.json", "r", encoding="utf-8") as file:
    complaints = json.load(file)

found = False

for record in complaints:
    if record["complaint_id"] == complaint_id:
        print("\n===== KISAN SUNAAI =====")
        print("Complaint:", record["complaint"])
        print("Category:", record["category"])
        print("Status:", record["status"])
        found = True
        break

if not found:
    print("Complaint not found!")

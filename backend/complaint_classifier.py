from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
)

complaint = "मुझे प्रधानमंत्री किसान योजना की किस्त नहीं मिली"

categories = [
    "PM Kisan payment issue",
    "Fertilizer shortage",
    "Crop damage",
    "Government scheme issue"
]

result = classifier(complaint, categories)

print("Complaint:", complaint)
print("Category:", result["labels"][0])
print("Confidence:", result["scores"][0])
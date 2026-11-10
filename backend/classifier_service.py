from transformers import pipeline

print("Loading Kisan Sunaai AI classifier...")

classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    device=-1
)

CATEGORIES = [
    "PM Kisan payment issue",
    "Fertilizer shortage",
    "Crop damage",
    "Government scheme issue",
    "Crop disease or pest problem",
    "Irrigation or water problem",
    "Other farmer problem"
]


def classify_complaint(complaint):
    prediction = classifier(complaint, CATEGORIES)

    return {
        "category": prediction["labels"][0],
        "confidence": round(float(prediction["scores"][0]), 2)
    }


print("Kisan Sunaai AI classifier loaded successfully!")
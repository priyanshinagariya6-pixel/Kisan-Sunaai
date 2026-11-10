
CATEGORIES = [
    "PM Kisan payment issue",
    "Fertilizer shortage",
    "Crop damage",
    "Government scheme issue",
    "Crop disease or pest problem",
    "Irrigation or water problem",
    "Other farmer problem"
]

KEYWORDS = {
    "PM Kisan payment issue": [
        "pm kisan", "installment", "kisth", "payment",
        "पैसा", "किस्त", "सम्मान निधि"
    ],
    "Fertilizer shortage": [
       "fertilizer", "urea", "khad", "khaad", "डीएपी",
        "खाद", "यूरिया"
    ],
    "Crop damage": [
        "crop damage", "fasal kharab", "baarish",
        "ओलावृष्टि", "फसल खराब", "नुकसान"
    ],
    "Government scheme issue": [
        "scheme", "yojana", "registration",
        "योजना", "रजिस्ट्रेशन"
    ],
    "Crop disease or pest problem": [
        "disease", "pest", "insect", "कीट",
        "रोग", "बीमारी", "फफूंद"
    ],
    "Irrigation or water problem": [
        "irrigation", "water", "paani", "sinchai",
        "पानी", "सिंचाई"
    ]
}


def classify_complaint(complaint):
    text = complaint.lower()

    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return {
                    "category": category,
                    "confidence": 0.85
                }

    return {
        "category": "Other farmer problem",
        "confidence": 0.50
    }

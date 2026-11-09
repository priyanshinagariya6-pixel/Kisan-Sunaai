from transformers import pipeline

classifier = pipeline("sentiment-analysis")

result = classifier("I am happy with the service")

print(result)
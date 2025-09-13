
from transformers import pipeline

# Load a zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

text = "The following article explores the impact of machine learning on modern medicine."

# You define the possible labels
labels = ["AI-generated", "Human-written"]

result = classifier(text, labels)

print(result)

example1.py
Displaying example.html.
import csv
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

input_file = "restaurant_reviews_120.csv"
output_file = "api_predictions.csv"

results = []

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for i, row in enumerate(reader, start=1):
        if i > 10:
            break

        print(f"Processing review {i}...")

        review = row["review_text"]

        prompt = f"""
Classify the sentiment of this restaurant review.

Only answer:
positive
or
negative

Review:
{review}
"""

        response = model.generate_content(prompt)

        prediction = response.text.strip().lower()

        if "positive" in prediction:
            prediction = "positive"
        elif "negative" in prediction:
            prediction = "negative"
        else:
            prediction = "unknown"

        results.append({
            "review_id": row["review_id"],
            "platform": row["platform"],
            "review_text": review,
            "true_label": row["true_label"],
            "predicted_label": prediction
        })

with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        "review_id",
        "platform",
        "review_text",
        "true_label",
        "predicted_label"
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in results:
        writer.writerow(row)

print(f"Saved predictions to {output_file}")
---
name: restaurant-review-evaluator
description: Uses the Gemini API to classify restaurant review sentiment from a CSV file, then evaluates the predictions with a deterministic Python script. Use this when the user asks to classify, evaluate, analyze, or audit restaurant review sentiment performance on tabular review data.
---

## When to use this skill

Use this skill when:
- The user provides a CSV file containing restaurant reviews
- The user wants to classify restaurant review sentiment using the Gemini API
- The user wants to evaluate sentiment classification performance
- The user asks for metrics such as accuracy, precision, recall, or F1 score
- The user wants to identify classification errors or misclassified examples
- The task involves structured tabular review data with ground-truth labels

---

## When NOT to use this skill

Do NOT use this skill when:
- The user asks for a general restaurant business strategy without review data
- The user wants the system to automatically reply to customers
- The user asks for final business decisions such as refunds, staff punishment, or compensation
- There is no structured CSV input
- The task is purely descriptive and does not require classification or evaluation
- The user wants to process private or sensitive customer data that should not be sent to an external API

---

## Expected inputs

The input should be a CSV file with at least the following columns:

- review_text: the content of the restaurant review
- true_label: the ground-truth sentiment label

Recommended columns include:
- review_id
- platform

The Gemini API classification script will generate:

- predicted_label: the model’s predicted sentiment label

Optional columns may include:
- rating
- date
- confidence
- issue_type

---

## Step-by-step instructions

1. Validate that the input is a CSV file.
2. Check that the required columns exist:
   - review_text
   - true_label
3. If predicted labels do not already exist, run the Gemini API classification script:
   - scripts/classify_reviews_api.py
4. The API classification script should:
   - read each review_text value
   - send the review to the Gemini API
   - ask the model to return only positive or negative
   - normalize the model output
   - save results to api_predictions.csv
5. Run the deterministic evaluation script:
   - scripts/evaluate_reviews.py
6. The evaluation script should:
   - load the prediction CSV
   - clean and normalize labels
   - compare true_label and predicted_label
   - compute accuracy, precision, recall, and F1 score
   - identify misclassified examples
7. Return a structured evaluation report.
8. Provide a short explanation of what the results mean for restaurant review monitoring.

---

## Expected output format

The output should include:

- total number of reviews processed
- number of valid rows used
- accuracy
- precision
- recall
- F1 score
- confusion summary
- misclassified examples, if any
- a short natural language summary of performance
- a short note about limitations and human review needs

---

## Limitations and checks

- This skill depends on the quality of the input review data and ground-truth labels.
- Gemini API predictions may vary slightly across runs.
- The current workflow supports binary sentiment classification: positive or negative.
- It may not handle sarcasm, mixed sentiment, multilingual reviews, or very short reviews perfectly.
- The skill should not be used to make automatic business decisions such as refunds, staff punishment, or compensation.
- Reviews containing private or sensitive customer information should be handled carefully before API processing.
- API keys must be stored in a .env file and should never be committed to GitHub.

---

## Role of the scripts

This skill uses two Python scripts.

### classify_reviews_api.py

This script is responsible for the GenAI classification step. It:
- reads restaurant reviews from the CSV file
- sends review_text to the Gemini API
- receives positive or negative predictions
- normalizes the output
- writes api_predictions.csv

### evaluate_reviews.py

This script is responsible for deterministic evaluation. It:
- parses and validates the prediction CSV
- compares true_label and predicted_label
- computes accuracy, precision, recall, and F1 score
- generates a confusion summary
- identifies misclassified examples

The Gemini API handles language understanding. The Python evaluation script handles exact numerical computation. This separation is important because natural language alone cannot reliably perform reproducible metric calculation.
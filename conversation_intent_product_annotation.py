"""
Conversation Intent and Product Annotation Tool

This script processes customer service conversations stored in an Excel file
and uses an external API to identify customer intent and related products.

Features:
- Reads conversation data from Excel
- Sends messages to an API for intent analysis
- Parses structured JSON responses
- Writes labeled results back to Excel

This project was developed during a Software Engineering Internship.
"""

import os
import time
import json
import re
import pandas as pd
import requests
from tqdm import tqdm


# ==============================
# Configuration
# ==============================

INPUT_FILE = "input_data.xlsx"
OUTPUT_FILE = "output_results.xlsx"
SHEET_NAME = "Sheet1"

INPUT_COLUMN = "chat_message"

OUTPUT_COLUMNS = [
    "product",
    "intent",
    "confidence",
    "analysis"
]

MAX_ROWS = 50

API_URL = "YOUR_API_ENDPOINT"

API_HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}


# ==============================
# Intent Configuration
# ==============================

SCENE_INTENTS = [
    "new_account",
    "change_plan",
    "cancel_service",
    "replace_sim",
    "international_roaming",
    "install_broadband",
    "price_too_high",
    "not_enough_data",
    "family_usage",
    "gaming_or_video_usage",
    "reject_no_need",
    "reject_already_have",
    "reject_enough",
    "data_demand_30_50GB",
    "data_demand_50_80GB",
    "data_demand_80_100GB",
    "data_demand_100_150GB",
    "data_demand_over_150GB",
    "live_alone",
    "family_size_small",
    "family_size_large",
    "travel_abroad",
    "agree_to_purchase",
    "poor_broadband_signal",
    "ask_broadband_price",
    "ask_plan_details",
    "compare_competitor_plans",
    "ask_discount",
    "ask_additional_benefits",
    "ask_secondary_sim",
    "ask_contract_phone",
    "ask_phone_model",
    "ask_installation_fee",
    "ask_data_voice_package",
    "ask_contract_length",
    "ask_price",
    "ask_usage_method",
    "ask_product_advantage",
    "ask_usage_location",
]

intent_lines = [f"{i+1}. {intent}" for i, intent in enumerate(SCENE_INTENTS)]

INTENT_PROMPT = "Intent List:\n" + "\n".join(intent_lines)


# ==============================
# System Prompt
# ==============================

SYSTEM_PROMPT = f"""
Task:
Analyze customer service conversation text and identify the customer's intent
and the related telecom product.

{INTENT_PROMPT}

Return the result in JSON format:

{{
  "product": "<product name or null>",
  "intent": "<identified intent>",
  "confidence": "high/medium/low",
  "analysis": "<short explanation>"
}}

If no product is mentioned, return null.
If no intent matches, return "other".
"""


# ==============================
# Safe API Call
# ==============================

def safe_api_call(payload, max_retries=5):

    backoff = 2

    for attempt in range(max_retries):

        try:

            response = requests.post(
                API_URL,
                headers=API_HEADERS,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            print(f"API call failed (attempt {attempt+1}). Retrying in {backoff}s...")

            time.sleep(backoff)

            backoff *= 2

    return None


# ==============================
# Intent Detection
# ==============================

def detect_intent(text):

    if not text or pd.isna(text):

        return {
            "product": None,
            "intent": "other",
            "confidence": "low",
            "analysis": "empty input"
        }

    payload = {
        "inputs": {
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": str(text)
        },
        "response_mode": "blocking",
        "user": "portfolio_demo"
    }

    result = safe_api_call(payload)

    if not result:

        return {
            "product": None,
            "intent": "other",
            "confidence": "low",
            "analysis": "API request failed"
        }

    raw_text = result.get("data", {}).get("outputs", {}).get("text", "").strip()

    try:

        parsed = json.loads(raw_text)

        if all(key in parsed for key in OUTPUT_COLUMNS):

            return parsed

    except:
        pass

    intent_match = re.search(r'"intent":\s*"([^"]+)"', raw_text)
    product_match = re.search(r'"product":\s*"([^"]+)"', raw_text)

    return {
        "product": product_match.group(1) if product_match else None,
        "intent": intent_match.group(1) if intent_match else "other",
        "confidence": "medium",
        "analysis": raw_text[:200]
    }


# ==============================
# Main Pipeline
# ==============================

def process_excel():

    if not os.path.exists(INPUT_FILE):

        print("Input file not found:", INPUT_FILE)

        return

    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)

    if INPUT_COLUMN not in df.columns:

        print("Missing column:", INPUT_COLUMN)

        return

    if len(df) > MAX_ROWS:

        df = df.head(MAX_ROWS)

    for col in OUTPUT_COLUMNS:

        df[col] = None

    print("Starting annotation process...")

    for idx, row in tqdm(df.iterrows(), total=len(df)):

        result = detect_intent(row[INPUT_COLUMN])

        for col in OUTPUT_COLUMNS:

            df.at[idx, col] = result.get(col)

        time.sleep(1)

    df.to_excel(OUTPUT_FILE, index=False)

    print("Annotation completed.")
    print("Results saved to:", OUTPUT_FILE)


# ==============================
# Run Script
# ==============================

if __name__ == "__main__":

    process_excel()

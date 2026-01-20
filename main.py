import requests
import os
from datetime import datetime

# -------------------------------
# User physical details (used by Nutritionix to estimate calories)
# -------------------------------
KG = 70          # Weight in kilograms
HEIGHT = 186     # Height in centimeters
AGE = 22         # Age in years

# -------------------------------
# API credentials (stored securely as environment variables)
# -------------------------------
APP_ID = os.environ["APP_ID"]        # Nutritionix App ID
API_KEY = os.environ["API_KEY"]      # Nutritionix API Key
DOMAIN = "https://trackapi.nutritionix.com/v2"

# -------------------------------
# Authentication details for workout tracking (e.g. Google Sheets / Sheety)
# -------------------------------
MY_USERNAME = os.environ["MY_USERNAME"]
MY_PASSWORD = os.environ["MY_PASSWORD"]

# -------------------------------
# API endpoints
# -------------------------------
query_endpoint = f"{DOMAIN}/natural/exercise"     # Nutritionix exercise parser
tracking_endpoint = os.environ["TRACKING_ENDPOINT"]  # Endpoint to store workout data

# -------------------------------
# HTTP headers required by Nutritionix API
# -------------------------------
header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

# -------------------------------
# Ask the user for exercise input (natural language)
# Example: "Ran 5km and cycled for 20 minutes"
# -------------------------------
query = input("Tell me which exercise you did?: ").title()

# -------------------------------
# Parameters sent to Nutritionix API
# -------------------------------
param = {
    "query": query,          # User-entered exercise description
    "weight_kg": KG,
    "height_cm": HEIGHT,
    "age": AGE
}

# -------------------------------
# Send exercise query to Nutritionix API
# -------------------------------
query_response = requests.post(
    url=query_endpoint,
    json=param,
    headers=header
)

# Convert response to Python dictionary
result = query_response.json()

# -------------------------------
# Get current date and time
# -------------------------------
now = datetime.now()
today_date = now.strftime("%d/%m/%Y")   # Format: DD/MM/YYYY
today_time = now.strftime("%H:%M:%S")   # Format: HH:MM:SS

# -------------------------------
# Loop through each detected exercise and log it
# -------------------------------
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # -------------------------------
    # Send workout data to tracking endpoint
    # -------------------------------
    tracking_response = requests.post(
        url=tracking_endpoint,
        json=sheet_inputs,
        auth=(MY_USERNAME, MY_PASSWORD)
    )

    # Raise an error if the request failed
    tracking_response.raise_for_status()

    # Print response from tracking API
    print(tracking_response.text)

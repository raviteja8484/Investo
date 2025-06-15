import json
from datetime import datetime, timedelta
from pathlib import Path
import os

DATA_FILE = Path("database/data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_contribution(name, amount, contribution_date, interest_rate):
    data = load_data()

    # Convert annual interest rate to monthly interest rate
    monthly_rate = interest_rate / 12 / 100
    interest_amount = round(amount * monthly_rate, 2)
    total_amount = round(amount + interest_amount, 2)
    maturity_date = contribution_date + timedelta(days=31)

    data.append({
        "name": name,
        "amount": amount,
        "contribution_date": contribution_date.isoformat(),
        "interest_rate": interest_rate,
        "interest_amount": interest_amount,
        "total_amount": total_amount,
        "maturity_date": maturity_date.isoformat(),
        "timestamp": datetime.now().isoformat()
    })
    save_data(data)
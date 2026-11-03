import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Data directory setup
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "train_delays.csv"

np.random.seed(42)

# Real major Indian trains with accurate routes and types
trains_master = [
    {"train_no": 12951, "train_name": "Mumbai Rajdhani", "origin": "Mumbai", "destination": "Delhi", "scheduled": 950, "distance": 1384},
    {"train_no": 12301, "train_name": "Howrah Rajdhani", "origin": "Howrah", "destination": "New Delhi", "scheduled": 1020, "distance": 1447},
    {"train_no": 12123, "train_name": "Sinhagad Express", "origin": "Mumbai", "destination": "Pune", "scheduled": 190, "distance": 192},
    {"train_no": 12124, "train_name": "Deccan Queen", "origin": "Pune", "destination": "Mumbai", "scheduled": 185, "distance": 192},
    {"train_no": 12050, "train_name": "Gatimaan Express", "origin": "Delhi", "destination": "Agra", "scheduled": 100, "distance": 188},
    {"train_no": 12639, "train_name": "Chennai Express", "origin": "Bangalore", "destination": "Chennai", "scheduled": 360, "distance": 362},
    {"train_no": 20901, "train_name": "Vande Bharat Exp", "origin": "Ahmedabad", "destination": "Mumbai", "scheduled": 320, "distance": 491},
    {"train_no": 12259, "train_name": "Sealdah Duronto", "origin": "Kolkata", "destination": "Delhi", "scheduled": 840, "distance": 1450},
    {"train_no": 12625, "train_name": "Kerala Express", "origin": "Trivandrum", "destination": "New Delhi", "scheduled": 3150, "distance": 3032},
    {"train_no": 12953, "train_name": "August Kranti Raj", "origin": "Mumbai", "destination": "Delhi", "scheduled": 980, "distance": 1378},
    {"train_no": 12002, "train_name": "Bhopal Shatabdi", "origin": "New Delhi", "destination": "Bhopal", "scheduled": 485, "distance": 703},
    {"train_no": 12655, "train_name": "Navajeevan Express", "origin": "Ahmedabad", "destination": "Chennai", "scheduled": 2100, "distance": 1950},
    {"train_no": 12955, "train_name": "Mumbai Express", "origin": "Mumbai", "destination": "Jaipur", "scheduled": 1150, "distance": 1150},
    {"train_no": 12393, "train_name": "Sampoorna Kranti", "origin": "Patna", "destination": "New Delhi", "scheduled": 720, "distance": 1001}
]

# Generate records for the past 2 years (approx 730 days) without duplicate entries per day
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
current_date = start_date

data = []

while current_date <= end_date:
    for t in trains_master:
        delay = int(np.random.exponential(scale=18))
        actual = t["scheduled"] + delay
        
        data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "train_no": t["train_no"],
            "train_name": t["train_name"],
            "origin": t["origin"],
            "destination": t["destination"],
            "scheduled_minutes": t["scheduled"],
            "actual_minutes": actual,
            "distance_km": t["distance"]
        })
    current_date += timedelta(days=1)

df = pd.DataFrame(data)
df.to_csv(DATA_FILE, index=False)
print(f"✅ Success! Generated {len(df):,} clean and realistic rows inside {DATA_FILE}")
import os
import json
import random
import time
from datetime import datetime

os.makedirs("data/", exist_ok=True)
DATA_PATH = "data/daily_feed.json"

users = [f"user_{i:03}" for i in range(1, 11)]

def generate_transaction():
    sender = random.choice(users)
    receiver = random.choice([u for u in users if u != sender])
    amount = round(random.uniform(1000, 2_000_000), 2)

    return {
        "transaction_id": f"TXN{random.randint(1000,9999)}",
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }

def append_transaction():
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    txn = generate_transaction()
    data.append(txn)

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[SIMULATOR] Added: {txn['transaction_id']} from {txn['sender']} to {txn['receiver']} ₹{txn['amount']}")

if __name__ == "__main__":
    while True:
        append_transaction()
        time.sleep(5)  # generates 1 txn every 5 seconds
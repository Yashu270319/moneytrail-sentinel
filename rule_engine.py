from collections import defaultdict

HIGH_VALUE_THRESHOLD = 1000000
REPEATED_RECEIVER_THRESHOLD = 3

import json

def load_blacklist(path="suspects/blacklist.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(json.load(f)["blacklisted_users"])
    except:
        return set()

def detect_suspicious_transactions(transactions):
    suspicious = []
    seen = {}
    blacklist = load_blacklist()

    for txn in transactions:
        reasons = []
        sender = txn["sender"]
        receiver = txn["receiver"]
        amount = txn["amount"]

        # Rule 1: High-value transaction
        if amount > 1_000_000:
            reasons.append("HIGH_VALUE")

        # Rule 2: Repeated receiver
        key = (sender, receiver)
        seen[key] = seen.get(key, 0) + 1
        if seen[key] > 3:
            reasons.append("REPEATED_RECEIVER")

        # Rule 3: Involves blacklisted user
        if sender in blacklist:
            reasons.append("BLACKLISTED_SENDER")
        if receiver in blacklist:
            reasons.append("BLACKLISTED_RECEIVER")

        if reasons:
            txn["reasons"] = reasons
            suspicious.append(txn)

    return suspicious
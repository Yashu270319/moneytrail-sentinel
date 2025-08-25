import os
from datetime import datetime

SUSPENSION_FILE = "logs/suspended_accounts.txt"

def suspend_accounts(transactions):
    """Suspends flagged senders involved in suspicious transactions."""
    suspended_users = set()

    # Load already suspended users
    if os.path.exists(SUSPENSION_FILE):
        with open(SUSPENSION_FILE, "r", encoding="utf-8") as f:
            for line in f:
                user = line.strip().split()[0]
                suspended_users.add(user)

    new_suspensions = []

    for txn in transactions:
        sender = txn["sender"]
        if sender not in suspended_users:
            new_suspensions.append(sender)
            suspended_users.add(sender)

    # Log new suspensions
    if new_suspensions:
        with open(SUSPENSION_FILE, "a", encoding="utf-8") as f:
            for user in new_suspensions:
                f.write(f"{user} suspended on {datetime.now().isoformat()}\n")

        print(f"[ACTION] Suspended {len(new_suspensions)} accounts.")
    else:
        print("[INFO] No new accounts suspended.")

    return new_suspensions
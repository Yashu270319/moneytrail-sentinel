import os
from datetime import datetime

LOG_DIR = "logs"

def log_suspicious_transactions(transactions):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filename = f"alerts_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(LOG_DIR, log_filename)

    # Use encoding="utf-8"
    with open(log_path, "a", encoding="utf-8") as f:
        for txn in transactions:
            f.write(
                f"[{datetime.now().isoformat()}] "
                f"TXN_ID: {txn['transaction_id']} | "
                f"FROM: {txn['sender']} -> TO: {txn['receiver']} | "
                f"AMOUNT: ₹{txn['amount']} | "
                f"REASONS: {', '.join(txn['reasons'])}\n"
            )

    print(f"[INFO] Logged {len(transactions)} suspicious transactions to {log_path}")
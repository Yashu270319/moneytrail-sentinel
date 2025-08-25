import json
from typing import List, Dict

def load_transactions(path: str = "data/daily_feed.json") -> List[Dict]:
    """
    Loads the transaction list from the specified JSON file.

    Args:
        path (str): Path to the JSON file containing transactions.

    Returns:
        List[Dict]: List of transaction dictionaries.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
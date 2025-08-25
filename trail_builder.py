import networkx as nx
from typing import List, Dict

def build_money_trail(transactions: List[Dict]) -> nx.DiGraph:
    """
    Constructs a directed graph representing the money trail.
    
    Each node represents a user (sender or receiver).
    Each directed edge represents a money transfer from sender → receiver,
    annotated with total amount and a list of involved transaction IDs.

    Args:
        transactions (List[Dict]): List of validated transaction dictionaries.

    Returns:
        nx.DiGraph: A directed graph modeling money flow.
    """
    G = nx.DiGraph()

    for txn in transactions:
        sender = txn["sender"]
        receiver = txn["receiver"]
        amount = txn["amount"]
        txn_id = txn["transaction_id"]

        # If an edge already exists, update the data
        if G.has_edge(sender, receiver):
            G[sender][receiver]["amount"] += amount
            G[sender][receiver]["transactions"].append(txn_id)
        else:
            G.add_edge(
                sender,
                receiver,
                amount=amount,
                transactions=[txn_id]
            )

    return G
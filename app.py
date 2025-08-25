import os
import sys
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Add root path to sys.path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from core.monitor import load_transactions
from core.rule_engine import detect_suspicious_transactions
from core.suspender import suspend_accounts
from core.logger import log_suspicious_transactions
from core.trail_builder import build_money_trail

# Enable auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="data_refresh")

# Load latest transactions
transactions = load_transactions()
flagged = detect_suspicious_transactions(transactions)
new_suspended = suspend_accounts(flagged)
log_suspicious_transactions(flagged)
G = build_money_trail(transactions)

# Streamlit App Config
st.set_page_config(page_title="Money Trail Sentinel", layout="wide")
st.title("🛡️ Money Trail Sentinel – Fraud Monitoring Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("📌 Total Transactions", len(transactions))
col2.metric("🚨 Suspicious Transactions", len(flagged))
col3.metric("🔒 Accounts Suspended", len(new_suspended))

st.divider()

# Breakdown of suspicious reasons
st.subheader("🧠 Suspicious Activity Breakdown")
reasons_count = Counter(reason for txn in flagged for reason in txn["reasons"])
if reasons_count:
    for reason, count in reasons_count.items():
        st.write(f"- {reason}: {count} cases")
else:
    st.write("✅ No suspicious transactions at this moment.")

# Show suspicious transaction table
st.subheader("📄 Flagged Transactions")
if flagged:
    st.dataframe(flagged, use_container_width=True)
else:
    st.write("✅ No flagged transactions detected yet.")

# Show all transactions
st.subheader("📄 All Transactions")
st.dataframe(transactions, use_container_width=True)

# Draw the money trail graph
st.subheader("🌐 Money Trail Network")

def draw_graph(G):
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color='#1976D2', node_size=1500, edgecolors='black', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_color='white', font_weight='bold', ax=ax)
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color='gray',
        arrowstyle='-|>',
        arrowsize=20,
        connectionstyle='arc3,rad=0.1',
        width=2,
        ax=ax
    )

    edge_labels = {
        (u, v): f"₹{data['amount']}" for u, v, data in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='darkred', ax=ax)

    ax.set_title("Money Trail Graph", fontsize=14, fontweight='bold')
    ax.axis('off')
    st.pyplot(fig)

draw_graph(G)
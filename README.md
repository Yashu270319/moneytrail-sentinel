# MoneyTrail Sentinel

A Python-based real-time financial fraud monitoring and automation system. This project simulates ongoing money transactions and flags suspicious behavior using predefined rules. It includes an interactive dashboard built with Streamlit for real-time monitoring and visualization.

## Features

- Generates real-time synthetic financial transactions
- Detects suspicious transactions using rule-based logic
- Automatically suspends high-risk accounts
- Logs all suspicious activities with timestamp
- Visualizes transaction trails as a network graph
- Supports blacklisting of specific users for tighter control

## Technologies Used

- Python 3.10+
- Streamlit (for the dashboard)
- NetworkX (for transaction graphs)
- Matplotlib
- JSON (for data storage and configuration)

## Detection Rules

- High-value transactions: Amounts over ₹10,00,000 are flagged
- Repeated receiver: More than 3 transactions to the same receiver from the same sender
- Blacklisted accounts: Any involvement of users in the blacklist triggers immediate flagging

## Project Structure
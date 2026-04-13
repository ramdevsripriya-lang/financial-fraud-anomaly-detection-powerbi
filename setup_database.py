import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def setup_database():
    db_name = "fraud_data.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop table if exists to start fresh
    cursor.execute("DROP TABLE IF EXISTS transactions")

    # Create table
    cursor.execute('''
        CREATE TABLE transactions (
            Transaction_ID INTEGER PRIMARY KEY,
            Amount REAL,
            Time TEXT,
            User_ID TEXT,
            Location TEXT,
            Is_Fraud INTEGER
        )
    ''')

    # 1. Data from the image
    image_data = [
        (1, 120.5, "10:05:00", "U101", "Delhi", 0),
        (2, 5000.0, "11:20:00", "U102", "Mumbai", 1),
        (3, 75.0, "12:15:00", "U103", "Hyderabad", 0),
        (4, 9999.9, "01:05:00", "U104", "Chennai", 1),
        (5, 250.0, "03:45:00", "U105", "Bangalore", 0),
        (6, 3000.0, "05:30:00", "U106", "Kolkata", 1),
        (7, 60.0, "07:10:00", "U107", "Pune", 0),
        (8, 15000.0, "09:50:00", "U108", "Delhi", 1)
    ]

    # 2. Additional Synthetic Data (to make ML training possible)
    np.random.seed(42)
    synthetic_data = []
    locations = ["Delhi", "Mumbai", "Hyderabad", "Chennai", "Bangalore", "Kolkata", "Pune"]
    
    for i in range(9, 101):
        user_id = f"U{np.random.randint(101, 120)}"
        location = np.random.choice(locations)
        amount = np.random.uniform(10, 15000)
        
        # Simple logic for synthetic fraud: high amount or early morning
        time_hour = np.random.randint(0, 24)
        time_str = f"{str(time_hour).zfill(2)}:{str(np.random.randint(0, 60)).zfill(2)}:00"
        
        is_fraud = 0
        if amount > 8000:
            is_fraud = np.random.choice([0, 1], p=[0.4, 0.6]) # High amount has higher fraud chance
        elif time_hour < 6:
            is_fraud = np.random.choice([0, 1], p=[0.7, 0.3]) # Early morning has some fraud chance
        else:
            is_fraud = np.random.choice([0, 1], p=[0.95, 0.05])
            
        synthetic_data.append((i, round(amount, 2), time_str, user_id, location, int(is_fraud)))

    # Combine data
    all_data = image_data + synthetic_data

    # Insert data
    cursor.executemany('''
        INSERT INTO transactions (Transaction_ID, Amount, Time, User_ID, Location, Is_Fraud)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', all_data)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' setup successfully with {len(all_data)} records.")

if __name__ == "__main__":
    setup_database()

# =========================================================
# FINANCIAL FRAUD & ANOMALY DETECTION 
# Tools: Pandas, NumPy, Matplotlib, Seaborn, SQLite
# =========================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
# --------------------------------------------------
# 1. SYNTHETIC DATA GENERATION (To setup the DB)
# --------------------------------------------------
print("[1] SETTING UP DATABASE...")
db_path = "fraud_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS transactions")
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
# Seed data for analysis
locations = ["Delhi", "Mumbai", "Hyderabad", "Chennai", "Bangalore", "Kolkata", "Pune"]
all_data = []
for i in range(1, 101):
    loc = np.random.choice(locations)
    amt = round(np.random.uniform(50, 15000), 2)
    is_fraud = 1 if amt > 12000 or (amt > 8000 and np.random.random() > 0.7) else 0
    time_str = f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}:00"
    all_data.append((i, amt, time_str, f"U{100+i}", loc, is_fraud))
cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", all_data)
conn.commit()
print("Database created successfully with 100 records.")
# --------------------------------------------------
# 2. DATA LOADING & INSPECTION
# --------------------------------------------------
print("\n[2] LOADING DATA...")
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()
print("Shape:", df.shape)
print("\nFirst 5 rows:")
display(df.head()) # 'display' works better than 'print' in Colab
# --------------------------------------------------
# 3. DATA CLEANING & TRANSFORMATION
# --------------------------------------------------
print("\n[3] CLEANING & TRANSFORMATION...")
# Fill missing, duplicates, etc.
df.drop_duplicates(inplace=True)
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(df['Amount'].mean())
# High amount marker
df['is_high_amount'] = df['Amount'].apply(lambda x: 1 if x > 4000 else 0)
# Map labels for charts
fraud_mapping = {0: 'Legitimate', 1: 'Fraudulent'}
df['Fraud_Status_Text'] = df['Is_Fraud'].map(fraud_mapping)
# Dummy Risk Score for trends
df['Risk_Score'] = (df['Amount'] / df['Amount'].max() * 50) + (df['Is_Fraud'] * 40) + np.random.randint(0, 10, size=len(df))
# --------------------------------------------------
# 4. DATA VISUALIZATION (PREMIUM STYLE)
# --------------------------------------------------
print("\n[4] GENERATING VISUALIZATIONS...")
plt.style.use('dark_background')
palette = {'Fraudulent': '#ff4b4b', 'Legitimate': '#00ffcc'}
# Chart 1: Fraud Counts by Location
plt.figure(figsize=(10, 5))
sns.countplot(x='Location', data=df[df['Is_Fraud']==1], palette='viridis')
plt.title('Fraud Cases by Location', color='#00ffcc', fontsize=14)
plt.show()
# Chart 2: Total Volume by Location
plt.figure(figsize=(10, 5))
df.groupby('Location')['Amount'].sum().plot(kind='bar', color='#00ffcc')
plt.title('Total Transaction Volume by Location', color='#00ffcc', fontsize=14)
plt.ylabel('Total Amount (₹)')
plt.show()
# Chart 3: Amount vs Risk Score
plt.figure(figsize=(10, 5))
sns.scatterplot(x='Amount', y='Risk_Score', hue='Fraud_Status_Text', data=df, palette=palette)
plt.title('Transaction Amount vs. Risk Score Trend', color='#00ffcc', fontsize=14)
plt.show()
# Chart 4: Amount Distribution
plt.figure(figsize=(8, 5))
sns.boxplot(x='Fraud_Status_Text', y='Amount', data=df, palette=palette)
plt.title('Amount Distribution by Fraud Status', color='#00ffcc', fontsize=14)
plt.show()
# --------------------------------------------------
# 5. EXPORT DATA
# --------------------------------------------------
output_file = "processed_fraud_data.xlsx"
df.to_excel(output_file, index=False)
print(f"\n[5] SUCCESS: Data exported to {output_file}")
print("PROJECT COMPLETED SUCCESSFULLY!")

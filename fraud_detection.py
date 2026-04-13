import sys
import subprocess
import os
import sqlite3

# --- Auto-install required libraries if they are missing ---
def install_and_import():
    required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn']
    
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import sklearn
    except ImportError:
        print("Missing libraries detected. Auto-installing them now, please wait...\n")
        for package in required_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception as e:
                print(f"Could not install {package}: {e}")
        print("\nAll libraries checked/installed successfully!\n")

install_and_import()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ---------------------------------------------------------
# 1. Load Data from SQLite Database
# ---------------------------------------------------------
def load_data_from_db():
    db_path = "fraud_data.db"
    if not os.path.exists(db_path):
        print(f"Error: Database '{db_path}' not found. Please run setup_database.py first.")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

print("Loading data from SQL database...")
df = load_data_from_db()

# ---------------------------------------------------------
# 2. Data Transformation (Simulating Power Query / DAX)
# ---------------------------------------------------------
print("Performing data transformations...")

# Power Query Logic equivalents
# h_Transact: High if Amount > 4000
df['h_Transact'] = df['Amount'].apply(lambda x: 'High' if x > 4000 else 'Normal')

# unusual_Ti: Unusual if Time is between 00:00 and 06:00
def check_unusual_time(time_str):
    try:
        hour = int(time_str.split(':')[0])
        return 'Unusual' if 0 <= hour <= 6 else 'Normal'
    except:
        return 'Normal'

df['unusual_Ti'] = df['Time'].apply(check_unusual_time)

# Fraud_Labe: Descriptive label for Is_Fraud
df['Fraud_Labe'] = df['Is_Fraud'].apply(lambda x: 'Fraud' if x == 1 else 'Non-Fraud')

# Handle missing values numerical
df['Amount'] = df['Amount'].fillna(df['Amount'].mean())

# Convert categorical data into numerical format using Label Encoding
label_encoders = {}
for col in ['Location', 'h_Transact', 'unusual_Ti', 'Fraud_Labe']:
    le = LabelEncoder()
    df[f'{col}_Encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le

# ---------------------------------------------------------
# 3. Exploratory Data Analysis (EDA)
# ---------------------------------------------------------
print("Generating analysis plots...")

# Plot 1: Amount vs Fraud Label
plt.figure(figsize=(8, 5))
sns.boxplot(x='Fraud_Labe', y='Amount', data=df, palette='Set2')
plt.title('Transaction Amount by Fraud Status')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig('amount_vs_fraud.png')
plt.close()

# Plot 2: Location-wise Fraud Frequency
plt.figure(figsize=(10, 6))
fraud_counts = df[df['Is_Fraud'] == 1].groupby('Location').size().reset_index(name='Counts')
sns.barplot(x='Location', y='Counts', data=fraud_counts, palette='viridis')
plt.title('Fraudulent Transactions by Location')
plt.xticks(rotation=45)
plt.savefig('location_fraud_counts.png')
plt.close()

print("Plots saved: 'amount_vs_fraud.png' and 'location_fraud_counts.png'\n")

# ---------------------------------------------------------
# 4. Machine Learning Model Setup
# ---------------------------------------------------------
# Define Features (X) and Target Label (y)
# We use the new flags (h_Transact, unusual_Ti) as features!
X = df[['Location_Encoded', 'Amount', 'h_Transact_Encoded', 'unusual_Ti_Encoded']]
y = df['Is_Fraud']

# Scale the continuous variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a Decision Tree Classifier
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X_train, y_train)

# ---------------------------------------------------------
# 5. Model Evaluation
# ---------------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("--- Model Evaluation ---")
print(f"Accuracy Score: {accuracy * 100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# ---------------------------------------------------------
# 6. Test Prediction Logic
# ---------------------------------------------------------
def predict_transaction(location, amount, time):
    loc_enc = label_encoders['Location'].transform([location])[0]
    h_trans = 'High' if amount > 4000 else 'Normal'
    h_trans_enc = label_encoders['h_Transact'].transform([h_trans])[0]
    unusual = check_unusual_time(time)
    unusual_enc = label_encoders['unusual_Ti'].transform([unusual])[0]
    
    input_data = np.array([[loc_enc, amount, h_trans_enc, unusual_enc]])
    input_scaled = scaler.transform(input_data)
    
    pred = model.predict(input_scaled)[0]
    return "Fraud" if pred == 1 else "Legitimate"

# Example test
test_loc = "Delhi"
test_amt = 15000
test_time = "09:50:00"
result = predict_transaction(test_loc, test_amt, test_time)
print(f"\n--- Sample Prediction ---")
print(f"Location: {test_loc}, Amount: ${test_amt}, Time: {test_time}")
print(f"Result: {result}")


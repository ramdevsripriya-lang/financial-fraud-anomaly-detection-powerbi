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
from sklearn.metrics import accuracy_score, classification_report

print("*" * 50)
print("PANDAS MINI PROJECT: CREDIT CARD FRAUD DETECTION")
print("*" * 50)

# ---------------------------------------------------------
#  1. Data Loading
# Reading data from files like CSV, Excel, SQL
# ---------------------------------------------------------
print("\n[1] DATA LOADING")
db_path = "fraud_data.db"
if not os.path.exists(db_path):
    print(f"Error: Database '{db_path}' not found. Please run setup_database.py first.")
    sys.exit(1)

conn = sqlite3.connect(db_path)
# Using read_sql_query (Pandas technique for SQL)
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()
print("Data loaded successfully from SQL Database into a DataFrame.")

# ---------------------------------------------------------
#  2. Data Inspection
# Understanding the dataset structure
# ---------------------------------------------------------
print("\n[2] DATA INSPECTION")
print("--> df.head(): First 3 rows")
print(df.head(3))

print("\n--> df.tail(): Last 2 rows")
print(df.tail(2))

print("\n--> df.info(): Understanding data types and non-null counts")
print(df.info())

print("\n--> df.describe(): Statistical summary of numerical columns")
print(df.describe())

# ---------------------------------------------------------
#  3. Data Cleaning
# Handling missing or incorrect data
# ---------------------------------------------------------
print("\n[3] DATA CLEANING")
# Renaming a column temporarily and changing it back to show rename()
df = df.rename(columns={'Amount': 'Transaction_Amount'})
print("Column renamed to 'Transaction_Amount'.")
df = df.rename(columns={'Transaction_Amount': 'Amount'}) # Change back for compatibility

# Filling missing values (fillna) - if any exist in 'Amount'
df['Amount'] = df['Amount'].fillna(df['Amount'].mean())

# Dropping entirely empty rows if any (dropna)
df = df.dropna(how='all')
print("Missing values filled and null rows dropped (if any).")

# ---------------------------------------------------------
#  4. Data Selection & Filtering
# Selecting specific rows/columns
# ---------------------------------------------------------
print("\n[4] DATA SELECTION & FILTERING")
print("--> Label-based selection (loc): Getting 'Location' & 'Amount' for first 3 rows")
print(df.loc[0:2, ['Location', 'Amount']])

print("\n--> Conditional filtering: Show transactions greater than 9000")
high_value_df = df[df['Amount'] > 9000]
print(f"Found {len(high_value_df)} high-value transactions.")

# ---------------------------------------------------------
#  5. Data Manipulation
# Modifying data, sorting, etc.
# ---------------------------------------------------------
print("\n[5] DATA MANIPULATION")
# Adding a new column
df['Risk_Level'] = 'Unknown'

# Sorting data
df = df.sort_values(by='Amount', ascending=False).reset_index(drop=True)
print("Data sorted by Amount (Descending). First 3 rows after sort:")
print(df[['Location', 'Amount']].head(3))

# ---------------------------------------------------------
#  6. Grouping & Aggregation
# Grouping data for analysis
# ---------------------------------------------------------
print("\n[6] GROUPING & AGGREGATION")
print("--> Average transaction amount per Location:")
avg_amount_by_loc = df.groupby('Location')['Amount'].mean().round(2)
print(avg_amount_by_loc)

# ---------------------------------------------------------
#  7. Merging & Joining
# Combining multiple datasets
# ---------------------------------------------------------
print("\n[7] MERGING & JOINING")
# Creating a dummy dataset to demonstrate merging
dummy_location_risk = pd.DataFrame({
    'Location': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai'],
    'City_Tier': ['Tier 1', 'Tier 1', 'Tier 1', 'Tier 1']
})
# Merge the DataFrames on 'Location'
df = df.merge(dummy_location_risk, on='Location', how='left')
# Fill missing City_Tier for other locations
df['City_Tier'] = df['City_Tier'].fillna('Other')
print(f"Merged DataFrame shape: {df.shape}")
print(df[['Location', 'City_Tier']].head(3))

# ---------------------------------------------------------
#  8. Data Transformation
# Changing data format
# ---------------------------------------------------------
print("\n[8] DATA TRANSFORMATION")
# apply() -> Apply a custom function
df['is_high_amount'] = df['Amount'].apply(lambda x: 1 if x > 4000 else 0)

# map() -> Mapping true/false to readable text
fraud_mapping = {0: 'Legitimate', 1: 'Fraudulent'}
df['Fraud_Status_Text'] = df['Is_Fraud'].map(fraud_mapping)

# astype() -> Changing data type from int to float for demonstration
df['Is_Fraud_Float'] = df['Is_Fraud'].astype(float)
print("Applied transformations (apply, map, astype).")
print(df[['Amount', 'is_high_amount', 'Is_Fraud', 'Fraud_Status_Text', 'Is_Fraud_Float']].head(3))

# ---------------------------------------------------------
#  9. Data Visualization
# Creating charts and graphs
# ---------------------------------------------------------
print("\n[9] DATA VISUALIZATION")
# Plotting using Seaborn & Matplotlib
plt.figure(figsize=(8, 5))
sns.boxplot(x='Fraud_Status_Text', y='Amount', data=df, palette='Set2')
plt.title('Transaction Amount by Fraud Status')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig('pandas_amount_vs_fraud.png')
plt.close()
print("Saved visualization to 'pandas_amount_vs_fraud.png'.")

# ---------------------------------------------------------
# 10. Exporting Data
# Saving processed data
# ---------------------------------------------------------
print("\n[10] EXPORTING DATA")
output_file = "processed_fraud_data.csv"
df.to_csv(output_file, index=False)
print(f"Successfully exported final clean dataset to '{output_file}'!")

print("\n" + "=" * 50)
print("✅ Pandas study techniques successfully strictly implemented!")
print("=" * 50 + "\n")

# --- ML Model Training (Optional extension from orig script) ---
print("Training a quick ML model on the processed data...")
le = LabelEncoder()
df['Location_Encoded'] = le.fit_transform(df['Location'])
X = df[['Location_Encoded', 'Amount']]
y = df['Is_Fraud']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Quick Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")

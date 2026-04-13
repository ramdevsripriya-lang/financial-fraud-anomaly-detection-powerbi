# financial-fraud-anomaly-detection-powerbi

💳 Financial Fraud & Anomaly Detection Dashboard using Power BI
📌 Project Overview

Financial fraud is one of the biggest challenges faced by banks, fintech companies, and online payment systems. This project focuses on detecting suspicious and unusual financial transactions using data analytics and visualization in Power BI.

The dashboard analyzes historical transaction data and applies statistical techniques to highlight anomalies, unusual spending patterns, and high-risk transactions in real time.

🎯 Project Objectives
Detect unusual or suspicious transactions.
Monitor customer spending behavior.
Identify high-risk accounts.
Help financial institutions reduce fraud losses.
Provide interactive visual insights for quick decision-making.
🏦 Where It Is Used

This system can be used in:

Banks and Credit Card Companies
FinTech & Payment Apps (UPI, Wallets)
E-commerce Platforms
Insurance Companies
Online Subscription Services
❗ Why This Project Is Important

Financial fraud causes billions of dollars in losses every year.
Manual monitoring is slow and inefficient.

This dashboard helps:

Detect fraud early
Reduce financial losses
Improve customer trust
Enable real-time monitoring
Support data-driven decisions
🧰 Tools & Technologies Used
Tool	Purpose
Power BI	Data visualization & dashboard creation
Excel / CSV Dataset	Transaction data source
Power Query	Data cleaning & transformation
DAX (Data Analysis Expressions)	Calculations & anomaly detection
Statistics	Mean, Standard Deviation, Z-Score
📊 Dataset Description

Typical dataset contains:

Transaction ID
Customer ID
Transaction Date & Time
Transaction Amount
Merchant Category
Location
Payment Method
Account Balance
Fraud Label (optional)
🔎 Fraud Detection Techniques Used
1️⃣ Statistical Anomaly Detection

We detect unusual transactions using:

Mean (Average)

Average transaction amount for a customer.

Standard Deviation

Measures how much spending varies.

Z-Score Formula
𝑍
=
𝑇
𝑟
𝑎
𝑛
𝑠
𝑎
𝑐
𝑡
𝑖
𝑜
𝑛
𝐴
𝑚
𝑜
𝑢
𝑛
𝑡
−
𝑀
𝑒
𝑎
𝑛
𝑆
𝑡
𝑎
𝑛
𝑑
𝑎
𝑟
𝑑
𝐷
𝑒
𝑣
𝑖
𝑎
𝑡
𝑖
𝑜
𝑛
Z=
StandardDeviation
TransactionAmount−Mean
	​


👉 If |Z| > 3, the transaction is considered Anomalous / Suspicious.

2️⃣ Spending Pattern Analysis

Detects:

Sudden high-value purchases
Unusual spending frequency
Spending spikes
Outlier transactions
3️⃣ Location-Based Detection

Flags transactions:

From unusual cities/countries
Multiple locations in short time
Impossible travel scenarios
4️⃣ Time-Based Detection

Detects transactions:

At unusual hours (late night)
Too many transactions in short time
Weekend/holiday spikes
📈 Dashboard Features
🔹 KPI Cards
Total Transactions
Total Amount Spent
Fraudulent Transactions Count
Fraud Percentage
🔹 Visual Charts
Transactions Over Time (Line Chart)
Fraud vs Normal (Pie Chart)
Spending by Category (Bar Chart)
Top Risk Customers (Table)
High-Risk Locations (Map)
🔹 Filters / Slicers
Date Range
Customer ID
Location
Merchant Category
Payment Method

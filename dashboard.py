import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import base64

# Page setup
st.set_page_config(page_title="Credit Card Fraud Analytics", layout="wide")

# Function to encode image to base64 for CSS background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    .title { 
        font-size: 48px !important; 
        font-weight: 800; 
        text-align: center; 
        color: #00ffcc; 
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 30px; 
    }
    
    .stMetric { 
        background: rgba(26, 26, 26, 0.8) !important; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #00ffcc;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.1);
    }

    /* Target metric label, value and delta for white color */
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricDelta"] div {
        color: #ff4b4b !important; /* Keep fraud rate red for visibility */
    }
    
    .stDataFrame {
        background: rgba(16, 16, 16, 0.8) !important;
        border-radius: 10px;
    }
    
    h1, h2, h3 { 
        color: #00ffcc !important; 
        text-shadow: 1px 1px 2px #000;
    }
    
    .stSidebar, .stSidebar p, .stSidebar label {
        background-color: rgba(10, 10, 10, 0.9) !important;
        color: white !important;
    }
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Try to set background
bg_path = "assets/bg.png"
if os.path.exists(bg_path):
    set_png_as_page_bg(bg_path)
else:
    # Fallback to dark solid background if image is missing
    st.markdown("""
<style>
    .stApp { background: #0a0a0a; color: #e0e0e0; }
    .title { font-size: 42px !important; font-weight: 800; text-align: center; color: #00ffcc; margin-bottom: 20px; }
</style>
    """, unsafe_allow_html=True)

# Database loading
def load_data():
    db_path = "fraud_data.db"
    if not os.path.exists(db_path):
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    
    # Apply logic for analytics (simulating DAX/Power Query)
    df['h_Transact'] = df['Amount'].apply(lambda x: 'High' if x > 4000 else 'Normal')
    df['unusual_Ti'] = df['Time'].apply(lambda x: 'Unusual' if 0 <= int(x.split(':')[0]) <= 6 else 'Normal')
    df['Fraud_Label'] = df['Is_Fraud'].apply(lambda x: 'Fraud' if x == 1 else 'Non-Fraud')
    
    return df

df = load_data()

if df.empty:
    st.error("No data found. Please run 'setup_database.py' and 'fraud_detection.py' first.")
    st.stop()

# Header
st.markdown("<h1 class='title'>🛡️ Credit Card Fraud & Anomaly Analytics</h1>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.title("🔍 Search & Filter")
locations = ["All"] + sorted(df['Location'].unique().tolist())
selected_loc = st.sidebar.selectbox("Select Location", locations)

if selected_loc != "All":
    filtered_df = df[df['Location'] == selected_loc]
else:
    filtered_df = df

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Transactions", len(filtered_df))
with col2:
    fraud_count = len(filtered_df[filtered_df['Is_Fraud'] == 1])
    st.metric("Fraud Cases", fraud_count, delta=f"{(fraud_count/len(filtered_df))*100:.1f}% Rate", delta_color="inverse")
with col3:
    high_val = len(filtered_df[filtered_df['h_Transact'] == 'High'])
    st.metric("High Volume", high_val)
with col4:
    unusual = len(filtered_df[filtered_df['unusual_Ti'] == 'Unusual'])
    st.metric("Unusual Hours", unusual)

st.divider()

# Main Dashboard Layout
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 Transaction Overview")
    st.dataframe(filtered_df.sort_values('Transaction_ID', ascending=False), use_container_width=True, hide_index=True)

with c2:
    st.subheader("📍 Fraud by Location")
    loc_fraud = df[df['Is_Fraud'] == 1].groupby('Location').size().reset_index(name='Count')
    fig_loc = px.pie(loc_fraud, values='Count', names='Location', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.Tealgrn, template="plotly_dark")
    st.plotly_chart(fig_loc, use_container_width=True)

# Analytics Section
st.divider()
st.subheader("🕵️ Advanced Anomaly Detection")
a_col1, a_col2 = st.columns(2)

with a_col1:
    st.markdown("### 💰 Amount vs. Fraud Visibility")
    fig_scatter = px.scatter(filtered_df, x="Amount", y="Location", color="Fraud_Label", 
                             size="Amount", hover_data=['User_ID', 'Time', 'h_Transact'],
                             color_discrete_map={'Fraud': '#ff4b4b', 'Non-Fraud': '#00ffcc'},
                             template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

with a_col2:
    st.markdown("### 🕒 Temporal Anomaly Analysis")
    # Extract hour for plotting
    filtered_df['Hour'] = filtered_df['Time'].apply(lambda x: int(x.split(':')[0]))
    fig_hist = px.histogram(filtered_df, x="Hour", color="unusual_Ti", barmode="overlay",
                            color_discrete_map={'Unusual': '#ff4b4b', 'Normal': '#00ffcc'},
                            template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)

# Prediction Interface
st.divider()
st.subheader("🚀 Real-time Fraud Prediction")
with st.expander("Evaluate New Transaction"):
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        p_amt = st.number_input("Transaction Amount", min_value=0.0, value=100.0)
    with p_col2:
        p_loc = st.selectbox("Transaction Location", sorted(df['Location'].unique().tolist()))
    with p_col3:
        p_time = st.time_input("Transaction Time")
    
    if st.button("Analyze Risk"):
        # Simple heuristic or could load the trained model if saved
        is_high = p_amt > 4000
        is_unusual = 0 <= p_time.hour <= 6
        
        risk_score = 0
        if is_high: risk_score += 40
        if is_unusual: risk_score += 40
        if p_amt > 10000: risk_score += 20
        
        if risk_score >= 60:
            st.error(f"⚠️ HIGH RISK DETECTED (Score: {risk_score}%)")
            st.warning("Logic: High amount combined with unusual timing.")
        elif risk_score >= 30:
            st.warning(f"🟡 MODERATE RISK (Score: {risk_score}%)")
        else:
            st.success(f"✅ LOW RISK (Score: {risk_score}%)")

st.markdown("---")
st.caption("Powered by SQL, Python Analytics & Data Science. Inspired by Power BI Logic.")


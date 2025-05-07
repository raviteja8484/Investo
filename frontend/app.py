import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.logic import add_contribution, load_data
# Add project root to sys.path

st.set_page_config(page_title="Investo Tracker", layout="wide")

st.title("📊 Investo Contribution Tracker")

# Form to add a new contribution
with st.form("contribution_form"):
    st.markdown("### 📥 Add Contribution")

    name = st.text_input("Contributor Name")
    amount = st.number_input("Amount (AED)", min_value=0.0, step=100.0)
    contribution_date = st.date_input("Date of Contribution")
    interest_rate = st.selectbox("Interest Rate (%)", [4.5, 6.0], index=0)

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name.strip():
            st.error("❌ Name is required.")
        elif amount <= 0:
            st.error("❌ Amount must be greater than 0.")
        elif not contribution_date:
            st.error("❌ Contribution date is required.")
        else:
            add_contribution(name, amount, contribution_date, interest_rate)
            st.success(f"✅ Added {amount} AED by {name} on {contribution_date} with {interest_rate}% interest.")

# Load and display data
df = pd.DataFrame(load_data())

if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["contribution_date"] = pd.to_datetime(df["contribution_date"])
    df["maturity_date"] = pd.to_datetime(df["maturity_date"])

    # Sort latest first
    df = df.sort_values(by="timestamp", ascending=False)

    # Summary metrics
    total_contributions = df["amount"].sum()
    total_interest = df["interest_amount"].sum()
    total_returns = df["total_amount"].sum()

    st.markdown("### 💵 Summary")
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Contributions", f"{total_contributions:,.2f} AED")
    col2.metric("💰 Interest Generated", f"{total_interest:,.2f} AED")
    col3.metric("💰 Returns", f"{total_returns:,.2f} AED")

    # Display the log table
    st.markdown("### 📋 Contribution Log")
    display_df = df.copy()
    display_df = display_df.rename(columns=lambda x: x.replace("_", " ").title())
    st.dataframe(display_df, use_container_width=True)

else:
    st.info("ℹ️ No contributions yet. Use the form above to add the first entry.")

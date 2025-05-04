"""Streamlit app for tracking WIO FD group investments using dummy JSON data."""


import json
import streamlit as st
import pandas as pd


# Load dummy data from JSON file
with open("dummy_data.json", "r",  encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

st.title("WIO FD Group Contribution Tracker (PoC)")

# Display the contribution table
st.subheader("Current Contributions")
st.dataframe(df)

# Total and progress bar
total = df["Amount (AED)"].sum()
GOAL = 35000
st.metric("Total Collected", f"AED {total}")
st.progress(min(total / GOAL, 1.0))

# Download options
st.subheader("Export Dummy Data")
json_data = json.dumps(data, indent=4)
csv_data = df.to_csv(index=False)

st.download_button("Download JSON", json_data, file_name="dummy_contributions.json")
st.download_button("Download CSV", csv_data, file_name="dummy_contributions.csv")

# Notes
st.info("This demo uses static dummy data with timestamps for each contribution.")

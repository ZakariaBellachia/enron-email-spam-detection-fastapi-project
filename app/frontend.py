import streamlit as st
import requests
import os

API_URL = os.getenv("BACKEND_URL", "http://backend:8000") + "/predict"


st.title("Email Classification App")
st.write("Enter the details of the email you want to classify:")
subject = st.text_input("Email Subject")
message = st.text_area("Email Message")
date = st.text_input("Date (YYYY-MM-DD)")
if st.button("Classify Email"):
    if not subject or not message or not date:
        st.error("Please fill in all fields.")
    else:
        email_data = {
            "subject": subject,
            "Message": message,
            "date": date
        }
        try:
            response = requests.post(API_URL, json=email_data)
            if response.status_code == 200:
                backend_message = response.json().get("message")
                st.success(backend_message)
            else:
                st.error("Error classifying the email. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")

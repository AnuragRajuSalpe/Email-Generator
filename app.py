import streamlit as st
import requests

# ✅ Paste your actual Gemini API key here
API_KEY = st.secrets["api_key"]  

# ✅ Gemini Flash endpoint
ENDPOINT = st.secrets["endpoint"]

st.title("Email Generator App")

# Initial state setup
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Input field for prompt
user_input = st.text_input("Enter your prompt to generate an email:")
prompt = f"Write a full and detailed email with subject, greeting, and closing — no templates or placeholders. Here is the request: {user_input}"

# Button to trigger generation
if st.button("Generate Email", disabled=st.session_state.processing):
    if not prompt.strip():
        st.error("⚠️ Please enter a valid prompt.")
    else:
        st.session_state.processing = True
        st.rerun()

# Processing the email generation
if st.session_state.processing and prompt:
    with st.spinner(" Generating Email..."):
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)

        st.session_state.processing = False  # Reset flag

        if response.status_code == 200:
            data = response.json()
            # ✅ Extract the email text safely from Gemini response structure
            try:
                email = data["candidates"][0]["content"]["parts"][0]["text"]
                st.success(" Email Generated Successfully!")
                st.text_area(" Generated Email:", value=email, height=300)
            except Exception as e:
                st.error(" Failed to extract email content from response.")
        else:
            st.error(f" API Error: {response.status_code} - {response.text}")


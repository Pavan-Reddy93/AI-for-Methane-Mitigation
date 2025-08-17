import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.oauth2 import service_account
import json

api_key = st.secrets.get("GOOGLE_API_KEY", None)

if api_key:
    # Preferred way: use Gemini API key
    genai.configure(api_key=api_key)
    st.session_state["genai_enabled"] = True
    st.write(" Connected to Google Generative AI with API key")
else:
    # Fallback: service account (for other GCP libs, not Gemini)
    if "google" in st.secrets and "credentials" in st.secrets["google"]:
        creds_dict = json.loads(st.secrets["google"]["credentials"])
        creds = service_account.Credentials.from_service_account_info(creds_dict)
        st.session_state["genai_enabled"] = False
        st.write(" No GOOGLE_API_KEY found. Using service account for GCP access.")
    else:
        st.session_state["genai_enabled"] = False
        st.warning(" No GOOGLE_API_KEY or service account credentials found in secrets.")


if "df" not in st.session_state:
    st.session_state.df = None

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to:",
    [
        "📂 Upload dataset",
        "⚙️ Select analysis options",
        "📊 Generate visualization",
        "🤖 Ask AI for report",
        "⬇️ Download insights",
    ]
)

if page == " Upload dataset":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success(" Dataset uploaded successfully!")
            st.write(st.session_state.df.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")


if page == " Select analysis options":
    if st.session_state.df is None:
        st.info(" Please upload a dataset first.")
    else:
        choice = st.selectbox(
            "Choose analysis type:",
            ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"]
        )

        if choice == "Descriptive Statistics":
            st.write(st.session_state.df.describe())
        elif choice == "Time Series Forecasting":
            st.write("⏳ Time series forecasting placeholder...")
        elif choice == "Correlation Analysis":
            try:
                st.write(st.session_state.df.corr())
            except Exception as e:
                st.error(f"Error running correlation: {e}")


if page == " Generate visualization":
    if st.session_state.df is None:
        st.info(" Please upload a dataset first.")
    else:
        st.write(" Visualization placeholder (charts will go here)...")


if page == " Ask AI for report":
    if st.session_state.df is None:
        st.info(" Please upload a dataset first.")
    elif not st.session_state.get("genai_enabled", False):
        st.warning(" AI report generation requires a GOOGLE_API_KEY in your secrets.")
    else:
        prompt = st.text_area("Enter your analysis request:")
        if st.button("Generate Report") and prompt.strip():
            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(prompt)
                st.subheader("AI Report")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI generation failed: {e}")


if page == " Download insights":
    if st.session_state.df is None:
        st.info(" Please upload a dataset first.")
    else:
        st.write(" Placeholder for downloadable insights...")


st.markdown(
    "---\n"
    "🌍 **AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization**  \
     Developed by *Ecothane Team - 1M1B Green Interns*"
)

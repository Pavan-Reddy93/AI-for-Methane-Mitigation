import streamlit as st
import google.generativeai as genai
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import pandas as pd
import io


st.set_page_config(page_title="AI for Methane Mitigation", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #f7faff;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 36px;
            color: #2c3e50;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #16a085;
            margin-bottom: 30px;
        }
        .nav {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }
        .nav button {
            background-color: #3498db;
            border: none;
            color: white;
            padding: 10px 20px;
            margin: 0 8px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .nav button:hover {
            background-color: #1abc9c;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: white;
            background-color: #2c3e50;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='title'> AI for Methane Mitigation</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A Dashboard for Emissions Forecasting and Biowaste Optimization</div>", unsafe_allow_html=True)


try:
    creds = service_account.Credentials.from_service_account_info(
        json.loads(st.secrets["google"]["credentials"]),
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    creds.refresh(Request())
    genai.configure(credentials=creds)
    st.success(" Connected to Google Generative AI using Service Account")
except Exception as e:
    st.error(f" Failed to authenticate with Google Service Account: {e}")



st.markdown("<div class='nav'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button(" Upload Dataset"):
        st.session_state.page = "upload"
with col2:
    if st.button(" Select Analysis Options"):
        st.session_state.page = "analysis"
with col3:
    if st.button(" Generate Visualization"):
        st.session_state.page = "visualize"
with col4:
    if st.button(" Ask AI for Report"):
        st.session_state.page = "report"
st.markdown("</div>", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "upload"

if st.session_state.page == "upload":
    st.subheader("Upload Your Dataset (CSV or PDF)")
    uploaded_file = st.file_uploader("Upload a file", type=["csv", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.write(" Preview of Uploaded CSV:")
            st.dataframe(df.head())
            st.session_state.df = df
        elif uploaded_file.type == "application/pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.text_area(" Extracted PDF Content:", text[:2000])
            st.session_state.pdf_text = text

elif st.session_state.page == "analysis":
    st.subheader("Select Analysis Options")
    options = st.multiselect("Choose analyses", ["Trend Forecasting", "Outlier Detection", "Descriptive Stats"])
    st.write("You selected:", options)

elif st.session_state.page == "visualize":
    if "df" in st.session_state:
        st.subheader("Generate Visualization")
        chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Area"])
        if chart_type == "Line":
            st.line_chart(st.session_state.df)
        elif chart_type == "Bar":
            st.bar_chart(st.session_state.df)
        elif chart_type == "Area":
            st.area_chart(st.session_state.df)
    else:
        st.warning(" Please upload a CSV dataset first.")

elif st.session_state.page == "report":
    st.subheader("AI-Powered Report Generator")
    user_prompt = st.text_area("Enter your analysis prompt:")
    if st.button("Generate Report"):
        if user_prompt:
            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(user_prompt)
                st.success(" AI Report Generated:")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI report generation failed: {e}")
        else:
            st.warning(" Please enter a prompt.")


st.markdown("<div class='footer'>Developed by Ecothane Team - 1M1B Green Interns</div>", unsafe_allow_html=True)

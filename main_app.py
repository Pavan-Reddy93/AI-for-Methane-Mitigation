import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import json


st.set_page_config(page_title="AI for Methane Mitigation", layout="wide")

# Try to load Google API key or service account
api_key = st.secrets.get("GOOGLE_API_KEY", None)

if api_key:
    genai.configure(api_key=api_key)
    ai_ready = True
else:
    try:
        google_creds = json.loads(st.secrets["google"]["credentials"])
        ai_ready = True
        st.warning(" No GOOGLE_API_KEY found. Using service account for GCP access.")
    except Exception:
        ai_ready = False
        st.error(" Google API not configured. AI features disabled.")

st.markdown("""
    <style>
    /* Global background */
    body {
        background: linear-gradient(135deg, #f0f8ff, #e6ffe6);
    }
    /* Title */
    h1 {
        text-align: center;
        color: #0d47a1;
        font-weight: 800;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(90deg, #1e88e5, #43a047);
        color: white !important;
    }
    /* Navigation buttons */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 20px;
        transition: all 0.3s ease;
        color: white;
        border: none;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    /* Assign different colors */
    #nav1 button { background-color: #1E90FF; }   /* Blue */
    #nav2 button { background-color: #FF8C00; }   /* Orange */
    #nav3 button { background-color: #32CD32; }   /* Green */
    #nav4 button { background-color: #8A2BE2; }   /* Purple */
    #nav5 button { background-color: #DC143C; }   /* Red */
    /* Footer */
    footer {
        text-align: center;
        background: linear-gradient(90deg, #1E90FF, #32CD32);
        color: white;
        padding: 12px;
        border-radius: 8px;
        margin-top: 35px;
        font-size: 14px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization")

st.markdown("##  Navigation")
cols = st.columns(5)

if cols[0].button("📂 Upload dataset", key="nav1"):
    st.session_state.nav_choice = "Upload dataset"
if cols[1].button("⚙️ Select analysis options", key="nav2"):
    st.session_state.nav_choice = "Analysis options"
if cols[2].button("📊 Generate visualization", key="nav3"):
    st.session_state.nav_choice = "Visualization"
if cols[3].button("🤖 Ask AI for report", key="nav4"):
    st.session_state.nav_choice = "AI Report"
if cols[4].button("⬇️ Download insights", key="nav5"):
    st.session_state.nav_choice = "Download"

nav_choice = st.session_state.get("nav_choice", "Upload dataset")


if nav_choice == "Upload dataset":
    uploaded_file = st.file_uploader("📂 Upload a CSV file with emission data", type=["csv"])
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(" Dataset uploaded successfully!")

elif nav_choice == "Analysis options":
    if "df" in st.session_state:
        option = st.radio("Choose analysis type:", ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"])
        df = st.session_state.df
        if option == "Descriptive Statistics":
            st.write(df.describe())
        elif option == "Time Series Forecasting":
            st.info(" Time series forecasting placeholder...")
        elif option == "Correlation Analysis":
            try:
                st.write(df.corr(numeric_only=True))
                fig, ax = plt.subplots()
                cax = ax.matshow(df.corr(numeric_only=True), cmap="coolwarm")
                plt.colorbar(cax)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Correlation error: {e}")
    else:
        st.warning(" Please upload a dataset first.")

elif nav_choice == "Visualization":
    if "df" in st.session_state:
        df = st.session_state.df
        st.line_chart(df.select_dtypes(include='number'))
    else:
        st.warning(" Please upload a dataset first.")

elif nav_choice == "AI Report":
    if "df" in st.session_state and ai_ready:
        prompt = st.text_input("Enter your analysis request:")
        if st.button("Generate Report"):
            with st.spinner(" Generating report..."):
                try:
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(prompt)
                    st.subheader(f"Report generated for prompt: {prompt}")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI report error: {e}")
    elif not ai_ready:
        st.error(" AI not available. Configure GOOGLE_API_KEY or service account.")
    else:
        st.warning(" Please upload a dataset first.")

elif nav_choice == "Download":
    if "df" in st.session_state:
        csv = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button(" Download CSV", csv, "insights.csv", "text/csv", key="download-csv")
    else:
        st.warning(" Please upload a dataset first.")


st.markdown("""
<footer>
 Developed by Ecothane Team - 1M1B Green Interns
</footer>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import json


api_key = st.secrets.get("GOOGLE_API_KEY", None)
if api_key:
    genai.configure(api_key=api_key)
    ai_enabled = True
else:
    ai_enabled = False
    st.warning(" No GOOGLE_API_KEY found. AI reports will be disabled.")

st.set_page_config(page_title="AI for Methane Mitigation", layout="wide")


st.title("🌍 AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization")


st.header("Navigation")
nav = st.radio(
    "Go to:",
    [
        "📂 Upload dataset",
        "⚙️ Select analysis options",
        "📊 Generate visualization",
        "🤖 Ask AI for report" if ai_enabled else "(AI Report Disabled)",
        "⬇️ Download insights"
    ],
    horizontal=False,
    label_visibility="collapsed",
    index=0,
    key="nav_choice"
)


nav_colors = {
    "📂 Upload dataset": "#ffb703",
    "⚙️ Select analysis options": "#8ecae6",
    "📊 Generate visualization": "#219ebc",
    "🤖 Ask AI for report": "#9b5de5",
    "(AI Report Disabled)": "#999999",
    "⬇️ Download insights": "#fb8500"
}

st.markdown(
    f"""
    <style>
        div[role='radiogroup'] label span {{
            padding: 8px 16px;
            border-radius: 8px;
            display: inline-block;
            margin-bottom: 5px;
            color: white !important;
        }}
        {''.join([f"div[role='radiogroup'] label:nth-child({i+1}) span {{background-color: {c};}}" for i,c in enumerate(nav_colors.values())])}
    </style>
    """,
    unsafe_allow_html=True
)


if "df" not in st.session_state:
    st.session_state.df = None


if nav == " Upload dataset":
    uploaded = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded:
        st.session_state.df = pd.read_csv(uploaded)
        st.success(" Dataset uploaded successfully!")
        st.dataframe(st.session_state.df.head())

elif nav == " Select analysis options":
    if st.session_state.df is not None:
        option = st.selectbox("Choose analysis type:", ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"])
        if option == "Descriptive Statistics":
            st.write(st.session_state.df.describe())
        elif option == "Time Series Forecasting":
            st.info(" Time series forecasting placeholder…")
        elif option == "Correlation Analysis":
            numeric_df = st.session_state.df.select_dtypes(include=["float64", "int64"])
            if not numeric_df.empty:
                st.write(numeric_df.corr())
                fig = px.imshow(numeric_df.corr(), text_auto=True, title="Correlation Heatmap")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No numeric columns found for correlation analysis.")
    else:
        st.warning(" Please upload a dataset first.")

elif nav == " Generate visualization":
    if st.session_state.df is not None:
        col = st.selectbox("Select column for visualization", st.session_state.df.columns)
        fig = px.histogram(st.session_state.df, x=col, title=f"Distribution of {col}")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button(" Download visualization as CSV", st.session_state.df.to_csv(index=False), "visualization.csv")
    else:
        st.warning(" Please upload a dataset first.")

elif nav == " Ask AI for report" and ai_enabled:
    if st.session_state.df is not None:
        prompt = st.text_area("Enter your analysis request:")
        if st.button("Generate Report") and prompt:
            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(f"Analyze the following dataset:\n{st.session_state.df.head(20).to_csv()}\n\nUser request: {prompt}")
                st.subheader("AI-Generated Report:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error generating AI report: {e}")
    else:
        st.warning(" Please upload a dataset first.")

elif nav == " Download insights":
    if st.session_state.df is not None:
        st.download_button(" Download dataset as CSV", st.session_state.df.to_csv(index=False), "insights.csv")
    else:
        st.warning(" Please upload a dataset first.")


st.markdown(
    """
    <div style='text-align:center; padding:15px; margin-top:30px; border-radius:10px;
                background: linear-gradient(to right, #219ebc, #8ecae6); color:white;'>
        Developed by <b>Ecothane Team - 1M1B Green Interns</b>
    </div>
    """,
    unsafe_allow_html=True
)

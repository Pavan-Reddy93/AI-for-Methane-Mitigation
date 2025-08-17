import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI for Methane Mitigation",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #e0f7fa, #f1f8e9); }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #065f46, #10b981);
        padding: 20px 15px;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #fff;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton button {
        width: 100%;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 12px;
        color: white;
        border-radius: 12px;
        padding: 12px;
    }
    .upload-btn button { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .analysis-btn button { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .viz-btn button { background: linear-gradient(90deg, #10b981, #34d399); }
    .ai-btn button { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .download-btn button { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(90deg, #1e3a8a, #2563eb);
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
        z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-title'> Navigation</div>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.sidebar.button(" Upload dataset", key="upload", help="Upload CSV file"):
    st.session_state.page = "upload"

if st.sidebar.button(" Select analysis options", key="analysis", help="Choose type of analysis"):
    st.session_state.page = "analysis"

if st.sidebar.button(" Generate visualization", key="viz", help="Visualize dataset"):
    st.session_state.page = "viz"

if st.sidebar.button(" Ask AI for report", key="ai", help="Enter prompt to generate report"):
    st.session_state.page = "ai"

if st.sidebar.button(" Download insights", key="download", help="Download report"):
    st.session_state.page = "download"


st.markdown("<h1 style='text-align:center;'> AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization</h1>", unsafe_allow_html=True)

uploaded_file = None
if st.session_state.page == "upload":
    uploaded_file = st.file_uploader(" Upload a CSV file with emission data", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(" File uploaded successfully!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f" Error reading file: {e}")

elif st.session_state.page == "analysis":
    st.subheader(" Select Analysis Options")
    analysis_type = st.radio("Choose analysis type:", ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"])
    st.info(f" Selected: {analysis_type}")

elif st.session_state.page == "viz":
    st.subheader(" Generate Visualization")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        col_options = df.columns.tolist()
        x_axis = st.selectbox("Select X-axis:", col_options)
        y_axis = st.selectbox("Select Y-axis:", col_options)
        if st.button("Generate Chart"):
            fig = px.line(df, x=x_axis, y=y_axis, title="Visualization")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(" Please upload a dataset first.")

elif st.session_state.page == "ai":
    st.subheader(" Ask AI for Report")
    user_prompt = st.text_area("Enter your analysis request:")
    if st.button("Generate Report"):
        if user_prompt.strip():
            st.success(f" Report generated for prompt: {user_prompt}")
            st.write(" (AI report content will go here...)")
        else:
            st.warning(" Please enter a prompt first.")

elif st.session_state.page == "download":
    st.subheader(" Download Insights")
    st.download_button("Download Report (TXT)", "This is a sample report.", file_name="report.txt")


st.markdown("""
    <div class="footer">
         Developed by <b>Ecothane Team - 1M1B Green Interns</b>
    </div>
""", unsafe_allow_html=True)

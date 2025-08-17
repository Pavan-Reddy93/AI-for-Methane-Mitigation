import streamlit as st
import pandas as pd
import plotly.express as px
import base64


st.set_page_config(
    page_title="AI for Methane Mitigation",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
    <style>
    /* Global background */
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #f1f8e9);
    }

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

    /* Navigation Items */
    .nav-item {
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        text-align: center;
        justify-content: center;
    }

    .nav-item:nth-child(2) { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .nav-item:nth-child(3) { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
    .nav-item:nth-child(4) { background: linear-gradient(90deg, #10b981, #34d399); }
    .nav-item:nth-child(5) { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .nav-item:nth-child(6) { background: linear-gradient(90deg, #ef4444, #f87171); }

    .nav-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

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


st.sidebar.markdown("<div class='sidebar-title'>📌 Navigation</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='nav-item'>📂 Upload dataset</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='nav-item'>⚙️ Select analysis options</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='nav-item'>📊 Generate visualization</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='nav-item'>🤖 Ask AI for report</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='nav-item'>⬇️ Download insights</div>", unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center;'> AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization</h1>", unsafe_allow_html=True)


uploaded_file = st.file_uploader(" Upload a CSV file with emission data", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(" File uploaded successfully!")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f" Error reading file: {e}")
else:
    st.info(" Please upload a CSV file to start analysis.")


st.markdown("""
    <div class="footer">
         Developed by <b>Ecothane Team - 1M1B Green Interns</b>
    </div>
""", unsafe_allow_html=True)

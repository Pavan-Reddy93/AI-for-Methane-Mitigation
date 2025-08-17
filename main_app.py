import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

st.markdown("""
<style>
/* App Background */
.stApp {
  background: linear-gradient(135deg, #E0F7F1 0%, #E6F8FF 50%, #FFFFFF 100%) fixed;
}

/* Font */
html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Headings */
h1, h2, h3 {
  color: #064E3B;
  letter-spacing: 0.5px;
}
h1 { font-weight: 900; }
h2 { font-weight: 700; margin-top: 1rem; }
h3 { font-weight: 600; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #14532D 0%, #1E7D5A 60%, #4ADE80 100%);
  color: #ffffff;
  padding: 10px;
}
section[data-testid="stSidebar"] h2 {
  color: #F0FDF4 !important;
  font-size: 1.2rem;
  border-bottom: 1px solid #A7F3D0;
  padding-bottom: 6px;
  margin-bottom: 12px;
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
  background: linear-gradient(90deg, #22c55e 0%, #10b981 50%, #06b6d4 100%) !important;
  color: white !important;
  font-weight: bold !important;
  border-radius: 14px !important;
  border: none !important;
  padding: 0.6rem 1rem !important;
  transition: transform 0.1s ease, filter 0.2s ease;
  box-shadow: 0 8px 16px rgba(16,185,129,0.35);
}
.stButton>button:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

/* Sections */
div[data-testid="stVerticalBlock"] > div:has(.stMarkdown),
div[data-testid="stVerticalBlock"] > div:has(.stDataFrame),
div[data-testid="stVerticalBlock"] > div:has(.stPlotlyChart),
div[data-testid="stVerticalBlock"] > div:has(.stImage),
div[data-testid="stVerticalBlock"] > div:has(canvas) {
  background: #ffffff;
  border: 1px solid #d1fae5;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 128, 128, 0.08);
  margin-bottom: 20px;
}

/* File uploader */
[data-testid="stFileUploader"] section {
  border-radius: 14px !important;
  border: 2px dashed #86efac !important;
  background-color: #f0fdf4 !important;
}

/* Table headers */
.stDataFrame [data-testid="stTable"] th {
  background: #d1fae5 !important;
  color: #065f46 !important;
  font-weight: bold !important;
}

/* Footer */
footer {
  visibility: visible;
}
footer:after {
  content: '🌱 Developed by EcoThane Team - 1M1B Green Interns';
  display: block;
  text-align: center;
  color: #065f46;
  font-size: 14px;
  font-weight: 600;
  padding: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization")

# Load an online methane-related banner image
img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Methane-Emission.jpg/640px-Methane-Emission.jpg"
try:
    response = requests.get(img_url)
    st.image(BytesIO(response.content), use_column_width=True)
except:
    st.warning("Could not load banner image. Please check internet connection.")

st.write("Analyze methane and greenhouse gas emissions data, generate insights, and create downloadable reports.")


st.sidebar.header("📌 Navigation")
st.sidebar.markdown("- Upload your dataset")
st.sidebar.markdown("- Select analysis options")
st.sidebar.markdown("- Generate visualization")
st.sidebar.markdown("- Ask AI for report")
st.sidebar.markdown("- Download insights")


uploaded_file = st.file_uploader("📂 Upload a CSV file with emission data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔎 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Column selectors
    st.markdown("### 🛠️ Select Columns for Analysis")
    country_col = st.selectbox("Select Country Column", df.columns, index=0)
    year_col = st.selectbox("Select Year Column", df.columns, index=1)
    emission_col = st.selectbox("Select Emissions Column", df.columns, index=2)

    # Select country
    countries = df[country_col].dropna().unique()
    selected_country = st.selectbox("🌐 Select Country", countries)

    filtered_df = df[df[country_col] == selected_country]

    # Visualization
    fig = px.line(
        filtered_df,
        x=year_col,
        y=emission_col,
        title=f"Gas Emissions in {selected_country}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

 
    st.subheader("📝 Generate Report with AI")
    user_prompt = st.text_area("Enter your prompt (e.g., 'Summarize methane trends for India between 2000-2020')")
    
    if user_prompt:
        # Very basic "mock AI" summary – replace later with LLM call
        avg_emission = filtered_df[emission_col].mean()
        latest_year = filtered_df[year_col].max()
        ai_report = f"**AI Report based on prompt:** {user_prompt}\n\n"
        ai_report += f"- Country: {selected_country}\n"
        ai_report += f"- Time Period: {filtered_df[year_col].min()} - {latest_year}\n"
        ai_report += f"- Average {emission_col}: {avg_emission:.2f}\n"
        ai_report += f"- Observed trend: {'increasing 📈' if filtered_df[emission_col].iloc[-1] > filtered_df[emission_col].iloc[0] else 'decreasing 📉'}\n\n"
        ai_report += "⚡ This is an automatically generated report for policy insights and biowaste optimization."

        st.markdown(ai_report)

        # Download option
        st.download_button(
            label="⬇️ Download Report",
            data=ai_report.encode("utf-8"),
            file_name=f"{selected_country}_ai_report.txt",
            mime="text/plain"
        )
else:
    st.info("👉 Please upload a CSV file to start analysis.")

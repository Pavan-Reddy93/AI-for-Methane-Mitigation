import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
<style>
/* Background: soft green-blue gradient */
.stApp {
  background: linear-gradient(135deg, #E0F7F1 0%, #E6F8FF 50%, #FFFFFF 100%) fixed;
}

/* Font and text smoothness */
html, body, [class*="css"] {
  font-family: 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Headings */
h1, h2, h3 {
  color: #14532D;
  letter-spacing: 0.4px;
}
h1 { font-weight: 800; }
h2 { font-weight: 700; }
h3 { font-weight: 600; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #2E8B57 0%, #3CB371 50%, #98FB98 100%);
  color: #ffffff;
}
section[data-testid="stSidebar"] * {
  color: #f0fdf4 !important;
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
  filter: brightness(1.08);
  transform: translateY(-2px);
}

/* Cards / sections */
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
}

/* Input fields */
input, textarea, select {
  border-radius: 10px !important;
  border: 1px solid #bbf7d0 !important;
}
input:focus, textarea:focus, select:focus {
  border-color: #10b981 !important;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
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

/* Report textarea */
textarea {
  background: #064e3b !important;
  color: #d1fae5 !important;
  border-radius: 14px !important;
  border: 1px solid #10b981 !important;
}

/* Hide footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


st.title(" Gas Emission Analyzer")
st.write("Analyze greenhouse gas emissions data and visualize trends for sustainability insights.")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload a CSV file with gas emission data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("🔎 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Column selectors to make app flexible
    st.markdown("### 🛠️ Select Columns for Analysis")
    country_col = st.selectbox("Select Country Column", df.columns, index=0)
    year_col = st.selectbox("Select Year Column", df.columns, index=1)
    emission_col = st.selectbox("Select Emissions Column", df.columns, index=2)

    # Choose country
    countries = df[country_col].dropna().unique()
    selected_country = st.selectbox("🌐 Select Country", countries)

    # Filter dataframe
    filtered_df = df[df[country_col] == selected_country]

    # Plot line chart
    fig = px.line(
        filtered_df,
        x=year_col,
        y=emission_col,
        title=f"Gas Emissions in {selected_country}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Download button
    st.download_button(
        label="⬇️ Download Analysis Report",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_country}_emissions_report.csv",
        mime="text/csv"
    )
else:
    st.info("👉 Please upload a CSV file to start the analysis.")

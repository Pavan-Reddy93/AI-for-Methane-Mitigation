import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
<style>
/* Background */
.stApp {
  background: linear-gradient(135deg, #E0F7F1 0%, #E6F8FF 50%, #FFFFFF 100%) fixed;
  font-family: 'Inter', sans-serif;
}

/* Title */
h1, h2, h3 {
  color: #14532D;
  font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #064e3b, #0d9488);
    padding: 20px;
}

/* Sidebar heading */
.nav-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 15px;
}

/* Sidebar items */
.nav-item {
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    font-size: 16px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}
.nav-item:hover {
    background: rgba(255,255,255,0.3);
    transform: translateX(5px);
}

/* Cards */
div[data-testid="stVerticalBlock"] > div:has(.stMarkdown),
div[data-testid="stVerticalBlock"] > div:has(.stDataFrame),
div[data-testid="stVerticalBlock"] > div:has(.stPlotlyChart),
div[data-testid="stVerticalBlock"] > div:has(canvas) {
  background: #ffffff;
  border: 1px solid #d1fae5;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 128, 128, 0.08);
  margin-bottom: 20px;
}

/* Inputs */
input, textarea, select {
  border-radius: 10px !important;
  border: 1px solid #bbf7d0 !important;
}
input:focus, textarea:focus, select:focus {
  border-color: #10b981 !important;
  box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
}

/* Footer */
footer {
  visibility: visible;
}
footer:after {
  content: ' Developed by Ecothane Team - 1M1B Green Interns';
  display: block;
  text-align: center;
  padding: 10px;
  font-size: 14px;
  color: #065f46;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="nav-title">📌 Navigation</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">📂 Upload your dataset</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">⚙️ Select analysis options</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">📊 Generate visualization</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">🤖 Ask AI for report</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">⬇️ Download insights</div>', unsafe_allow_html=True)


try:
    st.image(
        "https://images.unsplash.com/photo-1509395176047-4a66953fd231?auto=format&fit=crop&w=1350&q=80",
        use_container_width=True,
        caption="Methane Emissions & Biowaste Optimization Dashboard"
    )
except:
    st.warning(" Could not load banner image. Please check your internet connection.")

st.title(" AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization")
st.write("Analyze methane and greenhouse gas emissions data, generate insights, and create downloadable reports.")


uploaded_file = st.file_uploader(" Upload a CSV file with emission data", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader(" Preview of Uploaded Data")
    st.dataframe(df.head())

    # Country filter
    if "Country" in df.columns and "Year" in df.columns and "Emissions" in df.columns:
        countries = df["Country"].unique()
        selected_country = st.selectbox(" Select Country", countries)

        filtered_df = df[df["Country"] == selected_country]

        fig = px.line(filtered_df, x="Year", y="Emissions",
                      title=f"Gas Emissions in {selected_country}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # AI Report Prompt
        st.subheader(" Ask AI for a Forensic Report")
        user_prompt = st.text_area("Enter your custom analysis request (e.g., 'Summarize methane trends in India')")
        if user_prompt:
            st.success(f" AI would generate a forensic-style report for: *{user_prompt}*")

        # Download option
        st.download_button(
            label=" Download Analysis Report",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{selected_country}_emissions_report.csv",
            mime="text/csv"
        )
    else:
        st.error(" CSV must contain `Country`, `Year`, and `Emissions` columns.")
else:
    st.info(" Please upload a CSV file to start analysis.")

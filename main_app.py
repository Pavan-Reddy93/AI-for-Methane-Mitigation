import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai


st.set_page_config(page_title="AI for Methane Mitigation", layout="wide")

# Configure AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


st.markdown("""
<style>
/* Background gradient */
.stApp {
  background: linear-gradient(135deg, #d4fc79, #96e6a1);
  font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1e3c72, #2a5298);
  color: white;
}
section[data-testid="stSidebar"] * {
  color: white !important;
  font-weight: 500;
}

/* Navigation buttons */
.nav-btn {
  display: block;
  width: 100%;
  padding: 12px;
  margin: 6px 0;
  border-radius: 12px;
  text-align: center;
  font-weight: bold;
  cursor: pointer;
  color: white !important;
}
.nav-upload { background-color: #f59e0b; }
.nav-analysis { background-color: #10b981; }
.nav-visual { background-color: #3b82f6; }
.nav-ai { background-color: #8b5cf6; }
.nav-download { background-color: #ef4444; }

/* Footer */
.footer {
  text-align: center;
  padding: 15px;
  margin-top: 30px;
  border-top: 2px solid #ccc;
  color: #1f2937;
  font-weight: bold;
  background: #bbf7d0;
  border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "upload"
if "df" not in st.session_state:
    st.session_state.df = None

st.sidebar.markdown("##  Navigation")

if st.sidebar.button(" Upload dataset", key="upload_btn", use_container_width=True):
    st.session_state.page = "upload"

# Show rest of navigation **only if dataset is uploaded**
if st.session_state.df is not None:
    if st.sidebar.button("⚙️ Select analysis options", key="analysis_btn", use_container_width=True):
        st.session_state.page = "analysis"
    if st.sidebar.button("📊 Generate visualization", key="visual_btn", use_container_width=True):
        st.session_state.page = "visual"
    if st.sidebar.button("🤖 Ask AI for report", key="ai_btn", use_container_width=True):
        st.session_state.page = "ai"
    if st.sidebar.button("⬇️ Download insights", key="download_btn", use_container_width=True):
        st.session_state.page = "download"


st.title("🌍 AI for Methane Mitigation: A Dashboard for Emissions Forecasting and Biowaste Optimization")
st.write("Analyze methane and greenhouse gas emissions data, generate insights, and create downloadable reports.")



# 1. UPLOAD DATA
if st.session_state.page == "upload":
    uploaded_file = st.file_uploader(" Upload a CSV file with emission data", type=["csv"])
    if uploaded_file is not None:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success(" Dataset uploaded successfully!")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.info(" Please upload a dataset to continue.")

# 2. ANALYSIS OPTIONS
elif st.session_state.page == "analysis":
    st.subheader(" Select Analysis Options")
    option = st.radio("Choose analysis type:", ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"])

    if option == "Descriptive Statistics":
        st.write(st.session_state.df.describe())

    elif option == "Time Series Forecasting":
        if "Year" in st.session_state.df.columns and "Emissions" in st.session_state.df.columns:
            fig = px.line(st.session_state.df, x="Year", y="Emissions", title="📈 Emissions Over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Dataset must contain 'Year' and 'Emissions' columns.")

    elif option == "Correlation Analysis":
        numeric_df = st.session_state.df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            st.write(numeric_df.corr())
            fig = px.imshow(numeric_df.corr(), text_auto=True, title="🔗 Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No numeric columns available for correlation analysis.")

# 3. VISUALIZATION
elif st.session_state.page == "visual":
    st.subheader(" Generate Visualization")
    countries = st.session_state.df["Country"].unique() if "Country" in st.session_state.df.columns else []
    if len(countries) > 0:
        selected_country = st.selectbox("Select Country", countries)
        filtered_df = st.session_state.df[st.session_state.df["Country"] == selected_country]
        fig = px.line(filtered_df, x="Year", y="Emissions", title=f"Gas Emissions in {selected_country}", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No 'Country' column found in dataset.")

# 4. AI REPORT
elif st.session_state.page == "ai":
    st.subheader(" Ask AI for Report")
    user_prompt = st.text_input("Enter your analysis request:")
    if st.button("Generate AI Report"):
        if user_prompt.strip() != "":
            try:
                model = genai.GenerativeModel("gemini-pro")
                prompt = f"You are an emissions analyst. Based on this dataset, {user_prompt}. Dataset preview:\n{st.session_state.df.head().to_string()}"
                response = model.generate_content(prompt)
                st.success(f"Report generated for prompt: {user_prompt}")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI report generation failed: {e}")
        else:
            st.error("Please enter a prompt.")

# 5. DOWNLOAD
elif st.session_state.page == "download":
    st.subheader(" Download Insights")
    st.download_button("Download Full Dataset", data=st.session_state.df.to_csv(index=False).encode("utf-8"), file_name="emissions_dataset.csv", mime="text/csv")


st.markdown("<div class='footer'> Developed by Ecothane Team - 1M1B Green Interns</div>", unsafe_allow_html=True)

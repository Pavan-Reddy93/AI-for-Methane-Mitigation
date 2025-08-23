import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import json
import PyPDF2


st.set_page_config(page_title="AI Data Analyzer", layout="wide")

# Try to load Google API key or service account
api_key = st.secrets.get("GOOGLE_API_KEY", None)

if api_key:
    genai.configure(api_key=api_key)
    ai_ready = True
else:
    try:
        google_creds = json.loads(st.secrets["google"]["credentials"])
        ai_ready = True
        st.warning("No GOOGLE_API_KEY found. Using service account for GCP access.")
    except Exception:
        ai_ready = False
        st.error("Google API not configured. AI features disabled.")


st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f7faff, #e8fff1);
    }
    h1 {
        text-align: center;
        color: white;
        font-weight: 800;
        padding: 15px;
        border-radius: 12px;
        background: linear-gradient(90deg, #4A90E2, #50C878);
    }
    /* Navigation bar */
    .nav-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
        gap: 15px;
    }
    .nav-button {
        background: #1E90FF;
        color: white !important;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .nav-button:hover {
        background: #32CD32;
        transform: scale(1.05);
    }
    .selected {
        background: #FF8C00 !important;
    }
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


st.title("AI Data Analyzer: Smart Insights from Your Files")


nav_options = ["Upload File", "Analysis Options", "Visualization", "AI Report", "Download"]
if "nav_choice" not in st.session_state:
    st.session_state.nav_choice = nav_options[0]

# Custom nav bar
nav_html = '<div class="nav-container">'
for option in nav_options:
    selected_class = "nav-button selected" if st.session_state.nav_choice == option else "nav-button"
    nav_html += f'<a href="?nav={option}" class="{selected_class}">{option}</a>'
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# Handle query param navigation
query_params = st.query_params
if "nav" in query_params and query_params["nav"] in nav_options:
    st.session_state.nav_choice = query_params["nav"]

nav_choice = st.session_state.nav_choice

if nav_choice == "Upload File":
    uploaded_file = st.file_uploader("Upload a file (CSV or PDF)", type=["csv", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            st.session_state.df = pd.read_csv(uploaded_file)
            st.success("CSV uploaded and loaded successfully!")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            st.session_state.pdf_text = pdf_text
            st.success("PDF uploaded successfully!")

elif nav_choice == "Analysis Options":
    if "df" in st.session_state:
        option = st.radio("Choose analysis type:", ["Descriptive Statistics", "Correlation Analysis"])
        df = st.session_state.df
        if option == "Descriptive Statistics":
            st.write(df.describe())
        elif option == "Correlation Analysis":
            try:
                st.write(df.corr(numeric_only=True))
                fig, ax = plt.subplots()
                cax = ax.matshow(df.corr(numeric_only=True), cmap="coolwarm")
                plt.colorbar(cax)
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Correlation error: {e}")
    elif "pdf_text" in st.session_state:
        st.info("Text extracted from PDF available for AI report.")
    else:
        st.warning("Please upload a file first.")

elif nav_choice == "Visualization":
    if "df" in st.session_state:
        df = st.session_state.df
        st.line_chart(df.select_dtypes(include='number'))
    else:
        st.warning("Please upload a dataset first.")

elif nav_choice == "AI Report":
    if (("df" in st.session_state) or ("pdf_text" in st.session_state)) and ai_ready:
        prompt = st.text_area("Enter your analysis prompt:", "Summarize the key insights.")
        if st.button("Generate Report"):
            with st.spinner("Generating AI report..."):
                try:
                    model = genai.GenerativeModel("gemini-pro")
                    input_text = ""
                    if "df" in st.session_state:
                        input_text = st.session_state.df.to_csv(index=False)
                    elif "pdf_text" in st.session_state:
                        input_text = st.session_state.pdf_text
                    response = model.generate_content(f"{prompt}\n\nData:\n{input_text[:2000]}")
                    st.subheader("AI-Generated Report")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"AI report error: {e}")
    elif not ai_ready:
        st.error("AI not available. Configure GOOGLE_API_KEY or service account.")
    else:
        st.warning("Please upload a file first.")

elif nav_choice == "Download":
    if "df" in st.session_state:
        csv = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "insights.csv", "text/csv", key="download-csv")
    elif "pdf_text" in st.session_state:
        txt = st.session_state.pdf_text.encode("utf-8")
        st.download_button("Download Text", txt, "document.txt", "text/plain", key="download-txt")
    else:
        st.warning("Please upload a file first.")

st.markdown("""
<footer>
Developed by Ecothane Team - 1M1B Green Interns
</footer>
""", unsafe_allow_html=True)

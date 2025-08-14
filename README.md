
# Gas Analyzer App

A Streamlit-based web application for analyzing and generating reports on gas measurement data.

##  Features
- Upload and process gas sensor data
- Generate real-time visual analysis
- Export results to downloadable reports
- Secure handling of credentials using `.streamlit/secrets.toml` (not stored in repo)

##  Project Structure
```

gas\_analyzer\_app/
├── .streamlit/         # Contains secrets.toml (not tracked in Git)
├── data/               # Sample or uploaded datasets
├── reports/            # Generated reports
├── main\_app.py         # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation



## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Pavan-Reddy93/gas_analyzer_app.git
   cd gas_analyzer_app


2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your secrets**:

   * Create `.streamlit/secrets.toml`
   * Add your credentials there, for example:

     ```toml
     [gcp_service_account]
     type = "service_account"
     project_id = "your-project-id"
     private_key_id = "xxxxxxxxxxxxxxxxxxxxxxxx"
     private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
     client_email = "your-email@project.iam.gserviceaccount.com"
     client_id = "xxxxxxxxxxxx"
     ```
   * **Do not commit this file to GitHub**.

##  Running the App

```bash
streamlit run main_app.py
```

##  Deployment to Streamlit Cloud

1. Push the repo to GitHub (without `secrets.toml`).
2. Go to [Streamlit Cloud](https://share.streamlit.io/), connect your GitHub repo, and deploy.
3. Add your secrets in the **Streamlit Cloud Settings** under the "Secrets" section.

##  Security Notes

1. All sensitive credentials are stored locally in `.streamlit/secrets.toml` or via Streamlit Cloud’s secrets manager.
2. Never commit actual credentials to GitHub.

---

## Authors: Kasara Pavan Sai Reddy(Member),Arijin(Member),Pavan Odela(Member),Vaidehi Sharma (Team Lead)
## License: MIT


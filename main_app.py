import io
import textwrap
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="AI for Methane Mitigation",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
/* Page background (no pure white) */
.stApp {
  background: radial-gradient(1200px 600px at 15% 15%, #0b3d3a 0%, #0f5132 35%, #0c2b36 70%, #06202A 100%) fixed;
  color: #E8FFF2;
}

/* Banner */
.banner {
  width: 100%;
  padding: 26px 20px;
  border-radius: 18px;
  background: linear-gradient(90deg, rgba(0,195,143,0.25), rgba(0,172,230,0.25));
  border: 1px solid rgba(16, 185, 129, 0.35);
  box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}
.banner h1 {
  margin: 0 0 6px 0;
  font-weight: 800;
  letter-spacing: .3px;
  color: #D8FFF0;
}
.banner p {
  color: #C6FFE4;
  margin: 0;
}

/* Cards (sections) */
.block-container div[data-testid="stVerticalBlock"] > div:has(.card),
.block-container div[data-testid="stVerticalBlock"] > div:has(.stDataFrame),
.block-container div[data-testid="stVerticalBlock"] > div:has(.stPlotlyChart) {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 18px 16px;
  backdrop-filter: blur(6px);
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0f766e 0%, #14532d 100%);
  color: #ecfeff;
}
section[data-testid="stSidebar"] * { color: #ecfeff !important; }

/* Navigation buttons row */
.nav-row { margin-bottom: 8px; }
.nav-btn button {
  width: 100%;
  font-weight: 800 !important;
  letter-spacing: .2px;
  border: none !important;
  padding: .65rem .85rem !important;
  border-radius: 14px !important;
  box-shadow: 0 10px 18px rgba(0,0,0,.20);
  transition: transform .08s ease, filter .15s ease;
}
.nav-btn button:hover { transform: translateY(-2px); filter: brightness(1.05); }

/* Individual nav colors */
#upload button { background: linear-gradient(90deg,#06b6d4,#22d3ee); color:#00262e !important; }
#analyze button { background: linear-gradient(90deg,#f59e0b,#f97316); color:#2e1300 !important; }
#viz button { background: linear-gradient(90deg,#10b981,#22c55e); color:#012014 !important; }
#askai button { background: linear-gradient(90deg,#8b5cf6,#a78bfa); color:#17002e !important; }
#download button { background: linear-gradient(90deg,#ef4444,#f43f5e); color:#2e000a !important; }

/* Inputs look brighter */
input, textarea, select {
  border-radius: 10px !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #E8FFF2 !important;
}
.stTextInput > div > div > input::placeholder { color: #d2fbea88 !important; }

/* File uploader */
[data-testid="stFileUploader"] section {
  border-radius: 14px !important;
  border: 2px dashed rgba(0,223,176,.55) !important;
  background: rgba(0,223,176,.08) !important;
}

/* Footer */
.footer {
  margin-top: 24px;
  padding: 14px 16px;
  border-radius: 14px;
  background: linear-gradient(90deg, #0ea5e9 0%, #10b981 60%, #84cc16 100%);
  color: #052e2b;
  font-weight: 800;
  text-align: center;
  border: 1px solid rgba(255,255,255,0.25);
}

/* Headings */
h2, h3 { color: #d1fae5; }
</style>
""", unsafe_allow_html=True)


if "view" not in st.session_state:
    st.session_state.view = "upload"
if "df" not in st.session_state:
    st.session_state.df = None
if "report_text" not in st.session_state:
    st.session_state.report_text = ""
if "chart_bytes" not in st.session_state:
    st.session_state.chart_bytes = None

def set_view(v):
    st.session_state.view = v


st.markdown(
    """
    <div class="banner">
      <h1>🌍 AI for Methane Mitigation: A Dashboard for Emissions Forecasting & Biowaste Optimization</h1>
      <p>Analyze methane & GHG datasets, generate interactive visuals, and create forensic-style reports on demand.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.write("")  # small spacer
c1, c2, c3, c4, c5 = st.columns([1,1,1,1,1])
with c1:
    st.markdown('<div id="upload" class="nav-btn">', unsafe_allow_html=True)
    st.button(" Upload dataset", key="nav_upload", on_click=set_view, args=("upload",))
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown('<div id="analyze" class="nav-btn">', unsafe_allow_html=True)
    st.button(" Select analysis", key="nav_analysis", on_click=set_view, args=("analysis",))
    st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown('<div id="viz" class="nav-btn">', unsafe_allow_html=True)
    st.button(" Generate visualization", key="nav_viz", on_click=set_view, args=("viz",))
    st.markdown("</div>", unsafe_allow_html=True)
with c4:
    st.markdown('<div id="askai" class="nav-btn">', unsafe_allow_html=True)
    st.button(" Ask AI for report", key="nav_ai", on_click=set_view, args=("ai",))
    st.markdown("</div>", unsafe_allow_html=True)
with c5:
    st.markdown('<div id="download" class="nav-btn">', unsafe_allow_html=True)
    st.button(" Download insights", key="nav_dl", on_click=set_view, args=("download",))
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")  # spacer


def load_csv_safely(uploaded):
    try:
        df = pd.read_csv(uploaded)
        return df
    except pd.errors.EmptyDataError:
        st.error("Uploaded file is empty.")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
    return None

def to_numeric_if_possible(series):
    try:
        return pd.to_numeric(series)
    except Exception:
        return series

def simple_forensic_summary(df: pd.DataFrame) -> str:
    lines = []
    lines.append("FORENSIC SUMMARY – Methane/Emission Dataset")
    lines.append("-" * 60)
    lines.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    lines.append(f"Columns: {', '.join(list(df.columns))}")
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        desc = df[num_cols].describe().T
        lines.append("\nNUMERIC PROFILE (selected):")
        for idx, row in desc.iterrows():
            lines.append(f"• {idx} | mean={row['mean']:.3f}, std={row['std']:.3f}, min={row['min']:.3f}, max={row['max']:.3f}")
    if "Country" in df.columns:
        lines.append("\nTOP COUNTRIES BY ROW COUNT:")
        cts = df["Country"].value_counts().head(10)
        for c, v in cts.items():
            lines.append(f"• {c}: {v} rows")
    if "Year" in df.columns:
        try:
            y = pd.to_numeric(df["Year"], errors="coerce").dropna()
            if not y.empty:
                lines.append(f"\nYEAR RANGE: {int(y.min())} – {int(y.max())}")
        except Exception:
            pass
    # Potential spikes
    if num_cols:
        for col in num_cols[:3]:
            s = df[col].dropna()
            if len(s) > 5:
                q3 = s.quantile(0.75)
                q1 = s.quantile(0.25)
                iqr = q3 - q1
                spikes = (s > q3 + 1.5*iqr).sum()
                if spikes:
                    lines.append(f"• Possible spikes in {col}: {spikes} outliers (IQR method)")
    lines.append("\nASSESSMENT: Data appears suitable for exploratory analysis and visualization. Verify units and metadata before forecasting.")
    return "\n".join(lines)

def try_genai_report(prompt: str, df: pd.DataFrame) -> str:
    """
    If GENAI_API_KEY exists in st.secrets, use google-genai; else fallback to local summary guided by prompt.
    """
    sample = df.head(25).to_csv(index=False)
    try:
        api_key = st.secrets.get("GENAI_API_KEY", None)
    except Exception:
        api_key = None

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            system = "You are a data analyst specializing in methane emissions. Return a clear, forensic-style report with bullet points and a crisp conclusion."
            user = f"Dataset sample (CSV):\n{sample}\n\nUser request: {prompt}\n\nFocus on trends, anomalies, top emitters, and any policy/mitigation implications."
            resp = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[{"role":"system","parts":[{"text":system}]},
                          {"role":"user","parts":[{"text":user}]}],
                config={"temperature":0.4}
            )
            # google-genai response can be in candidates[0].content.parts
            try:
                return resp.text.strip()
            except Exception:
                return str(resp)
        except Exception as e:
            return f"(Local fallback – API error: {e})\n\n" + simple_forensic_summary(df)
    else:
        # Local heuristic, guided by the prompt keywords
        base = simple_forensic_summary(df)
        extra = []
        p = prompt.lower()
        if "highest" in p or "max" in p:
            num_cols = df.select_dtypes(include="number").columns.tolist()
            if num_cols:
                col = num_cols[0]
                idx = df[col].idxmax()
                row = df.loc[idx].to_dict()
                extra.append(f"\nHIGHEST observed in '{col}': {df[col].max()} at row {int(idx)} (context: {row})")
        if "trend" in p or "increase" in p or "decrease" in p:
            if "Year" in df.columns:
                try:
                    y = pd.to_numeric(df["Year"], errors="coerce")
                    num_cols = df.select_dtypes(include="number").columns.tolist()
                    if len(num_cols) >= 1:
                        col = num_cols[0]
                        tmp = df[[col]].copy()
                        tmp["Year"] = y
                        tmp = tmp.dropna()
                        trend = "increasing" if tmp[col].corr(tmp["Year"]) > 0 else "decreasing"
                        extra.append(f"\nTREND: '{col}' appears {trend} with Year (corr={tmp[col].corr(tmp['Year']):.3f}).")
                except Exception:
                    pass
        if not extra:
            extra.append("\nNOTE: Prompt-specific analysis requires an API key for richer reasoning. Add GENAI_API_KEY in Streamlit Secrets.")
        return base + "\n" + "\n".join(extra)

def capture_plotly(fig) -> bytes:
    """Return a PNG bytes snapshot; if kaleido not available, return None gracefully."""
    try:
        import plotly.io as pio
        return pio.to_image(fig, format="png")
    except Exception:
        return None



if st.session_state.view == "upload":
    st.subheader(" Upload your dataset")
    up = st.file_uploader("Upload a CSV file with emission-related data", type=["csv"])
    if up is not None:
        df = load_csv_safely(up)
        if df is not None:
            st.session_state.df = df
            st.success("Dataset loaded and cached. You can switch tabs without re-uploading.")
            st.dataframe(df.head())

elif st.session_state.view == "analysis":
    st.subheader("⚙️ Select Analysis Options")
    if st.session_state.df is None:
        st.info("Please upload a dataset first ( Upload dataset).")
    else:
        df = st.session_state.df
        analysis = st.radio(
            "Choose analysis type:",
            ["Descriptive Statistics", "Time Series Forecasting", "Correlation Analysis"],
            horizontal=True
        )

        if analysis == "Descriptive Statistics":
            st.write("Summary:")
            st.dataframe(df.describe(include="all").T.fillna("").head(25))

        elif analysis == "Time Series Forecasting":
            st.caption("Simple preview forecasting (naive/rolling). For production, integrate Prophet/ARIMA.")
            cols = df.columns.tolist()
            x_col = st.selectbox("Date/Time or Year Column", options=cols, index=cols.index("Year") if "Year" in cols else 0)
            y_col = st.selectbox("Target (numeric) Column", options=df.select_dtypes(include="number").columns.tolist())
            if st.button("Run Quick Forecast"):
                try:
                    x_vals = pd.to_datetime(df[x_col], errors="coerce") if "year" not in x_col.lower() else pd.to_datetime(df[x_col].astype(str), errors="coerce", format="%Y")
                    y_vals = pd.to_numeric(df[y_col], errors="coerce")
                    tmp = pd.DataFrame({"ds": x_vals, "y": y_vals}).dropna().sort_values("ds")
                    if len(tmp) < 8:
                        st.warning("Not enough points to forecast.")
                    else:
                        tmp["y_roll"] = tmp["y"].rolling(3, min_periods=1).mean()
                        fig = px.line(tmp, x="ds", y=["y","y_roll"], title=f"Quick Trend: {y_col} over {x_col}")
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.chart_bytes = capture_plotly(fig)
                except Exception as e:
                    st.error(f"Forecasting failed: {e}")

        elif analysis == "Correlation Analysis":
            num_df = df.select_dtypes(include=["number"])
            if num_df.empty:
                st.warning("No numeric columns available for correlation.")
            else:
                corr = num_df.corr(numeric_only=True)
                fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
                st.plotly_chart(fig, use_container_width=True)

elif st.session_state.view == "viz":
    st.subheader(" Generate Visualization")
    if st.session_state.df is None:
        st.info("Please upload a dataset first ( Upload dataset).")
    else:
        df = st.session_state.df.copy()
        cols = df.columns.tolist()
        x_col = st.selectbox("X Axis", options=cols, index=cols.index("Year") if "Year" in cols else 0)
        y_col = st.selectbox("Y Axis (numeric preferred)", options=cols, index=1 if len(cols)>1 else 0)
        group_col = st.selectbox("Group/Color (optional)", options=["(none)"] + cols, index=0)
        chart_type = st.radio("Chart Type", ["Line","Bar","Scatter"], horizontal=True)

        # Auto-convert common fields
        if "year" in x_col.lower():
            try:
                df[x_col] = pd.to_numeric(df[x_col], errors="coerce")
            except Exception:
                pass
        df[y_col] = pd.to_numeric(df[y_col], errors="coerce")

        go_kwargs = {}
        if group_col != "(none)":
            go_kwargs["color"] = group_col

        fig = None
        try:
            if chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, markers=True, **go_kwargs, title=f"{y_col} vs {x_col}")
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, **go_kwargs, title=f"{y_col} by {x_col}")
            else:
                fig = px.scatter(df, x=x_col, y=y_col, **go_kwargs, title=f"{y_col} vs {x_col}")
        except Exception as e:
            st.error(f"Could not create chart: {e}")

        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.session_state.chart_bytes = capture_plotly(fig)
            csv_preview = df[[x_col, y_col]].dropna().to_csv(index=False).encode("utf-8")
            st.download_button(" Download chart data (CSV)", data=csv_preview, file_name="chart_data.csv", mime="text/csv")

elif st.session_state.view == "ai":
    st.subheader(" Ask AI for Report")
    if st.session_state.df is None:
        st.info("Please upload a dataset first ( Upload dataset).")
    else:
        prompt = st.text_area("Enter your analysis request:", value="highest emission recorded in country", height=120, placeholder="e.g., Compare methane trends by country since 2000 and flag top 5 spikes.")
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                report = try_genai_report(prompt, st.session_state.df)
                st.session_state.report_text = report
        if st.session_state.report_text:
            st.success("Report generated.")
            st.code(st.session_state.report_text, language="markdown")
            st.download_button(
                " Download forensic report (TXT)",
                data=st.session_state.report_text.encode("utf-8"),
                file_name="forensic_report.txt",
                mime="text/plain"
            )

elif st.session_state.view == "download":
    st.subheader(" Download Insights")
    if st.session_state.df is None:
        st.info("Please upload a dataset first ( Upload dataset).")
    else:
        if st.session_state.report_text:
            st.download_button(
                "Download latest report (TXT)",
                data=st.session_state.report_text.encode("utf-8"),
                file_name="forensic_report.txt",
                mime="text/plain"
            )
        else:
            st.info("No report generated yet (use  Ask AI for report).")

        if st.session_state.chart_bytes:
            st.download_button(
                "Download latest chart (PNG)",
                data=st.session_state.chart_bytes,
                file_name="chart.png",
                mime="image/png"
            )
        else:
            st.info("No chart captured yet (use  Generate visualization).")


st.markdown(
    '<div class="footer">Developed by <b>Ecothane Team</b> — <b>1M1B Green Interns</b></div>',
    unsafe_allow_html=True
)

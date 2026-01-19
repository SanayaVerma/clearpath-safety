import streamlit as st
import requests
import pandas as pd
from openai import OpenAI
import time

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="ClearPath Safety", page_icon="🚗", layout="wide")

st.markdown("""
    <style>
    @keyframes flashing { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    .flash-red { 
        background-color: #FF0000; color: white; padding: 20px; 
        border-radius: 10px; font-weight: bold; text-align: center;
        font-size: 24px; animation: flashing 1s infinite;
    }
    .warning-yellow { 
        background-color: #FFD700; color: black; padding: 20px; 
        border-radius: 10px; font-weight: bold; text-align: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Top-Level Summary
st.title("🚗 ClearPath Safety Assistant")
st.markdown("""
### Empowering Families and Communities with Smarter Safety Data
ClearPath Safety bridges the gap between technical federal databases and everyday drivers. 
By pulling live data from the **NHTSA** and using **Advanced AI**, we provide 
instant, plain-English clarity on vehicle safety risks that could save lives.
""")

# 3. Sidebar for API Key (Picked from Secrets)
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Enter OpenAI API Key (if not in secrets)", type="password")

# 4. User Input Section
st.subheader("🔍 Step 1: Enter Your Vehicle Information")
col1, col2, col3 = st.columns(3)
year = col1.text_input("Year", "2010")
make = col2.text_input("Make", "Toyota")
model = col3.text_input("Model", "Corolla")

if st.button("Generate Comprehensive Safety Audit"):
    if not api_key:
        st.error("Missing API Key. Please add it to Streamlit Secrets or the sidebar.")
    else:
        # 5. Progress Bar Setup
        progress_bar = st.progress(0, text="Initializing...")
        
        # Phase A: Download from NHTSA
        progress_bar.progress(25, text="Downloading records from NHTSA (Data.gov)...")
        url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
        response = requests.get(url)
        recalls = response.json().get('results', [])
        time.sleep(1) # Visual pause for the demo

        if not recalls:
            progress_bar.progress(100, text="Completed.")
            st.success(f"✅ No active recalls found for the {year} {make} {model}!")
        else:
            # 6. Tabulated Data (Index starting from 1)
            st.subheader("📋 Official Recall Notices")
            df = pd.DataFrame(recalls)
            df.index = range(1, len(df) + 1)  # Set index to start from 1
            st.dataframe(df, use_container_width=True)

            # 7. Download Link for CSV
            csv = df.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="📥 Download Raw Data as CSV",
                data=csv,
                file_name=f"{year}_{make}_{model}_recalls.csv",
                mime="text/csv",
            )

            # Phase B: AI Generation
            progress_bar.progress(60, text="AI is evaluating safety risks and generating your summary...")
            client = OpenAI(api_key=api_key)
            combined_descriptions = "\n".join([f"- {r['Component']}: {r['Summary']}" for r in recalls])

            # Updated AI Analysis Prompt
prompt = f"""
You are a Senior Automotive Safety Expert. Your goal is to provide an objective risk assessment.
Analyze these recalls for a {year} {make} {model}:
{combined_desc}

### CLASSIFICATION RUBRIC:
- **RED (Critical):** Assign ONLY if there is a direct risk of:
    - Fire or fuel leaks.
    - Loss of steering or braking control.
    - Engine stalling while driving at high speeds.
    - Airbag malfunctions (shrapnel or non-deployment).
    - Wheels or structural components breaking.

- **YELLOW (Cautionary):** Assign for all other safety issues, such as:
    - Interior lighting or visibility issues.
    - Minor sensors or software glitches that don't stop the car.
    - Improper labeling or owner's manual errors.
    - Seat adjustment or non-structural interior trim.
    - Backup camera glitches (unless primary visibility is lost).

### EXAMPLES FOR CALIBRATION:
- "Sun visor may detach" -> YELLOW
- "Fuel pump failure may cause engine stall" -> RED
- "Inaccurate tire pressure label" -> YELLOW
- "Brake booster loses vacuum" -> RED

### YOUR TASK:
1. Evaluate the recalls. If even ONE recall meets the RED criteria, the VERDICT is RED.
2. Provide a 3-sentence summary. Be calm and factual. Do not exaggerate.

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
VERDICT: [RED or YELLOW]
SUMMARY: [Text]
"""
            ai_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            
            full_text = ai_response.choices[0].message.content
            risk_color = "RED" if "VERDICT: RED" in full_text.upper() else "YELLOW"
            summary = full_text.split("SUMMARY:")[-1].strip()

            # Finalize Progress
            progress_bar.progress(100, text="Safety Audit Complete.")
            time.sleep(0.5)
            progress_bar.empty()

            # 8. Visual Warning Sign & Verdict
            st.subheader("⚠️ AI Safety Verdict")
            if risk_color == "RED":
                st.markdown('<div class="flash-red">🚨 CRITICAL RISK: IMMEDIATE ACTION REQUIRED 🚨</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-yellow">⚠️ CAUTION: SAFETY REPAIRS RECOMMENDED ⚠️</div>', unsafe_allow_html=True)
            
            st.info(f"**Expert Analysis:** {summary}")



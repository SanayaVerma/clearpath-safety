import streamlit as st
import requests
import pandas as pd
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="ClearPath Safety", page_icon="🚗", layout="wide")

# Custom CSS for the "Flashing" and Alert effects
st.markdown("""
    <style>
    @keyframes flashing { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .flash-red { color: white; background-color: #FF0000; padding: 15px; border-radius: 10px; 
                 font-weight: bold; text-align: center; animation: flashing 1s infinite; }
    .warning-yellow { color: black; background-color: #FFD700; padding: 15px; 
                      border-radius: 10px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 ClearPath Safety Assistant")

# Sidebar for API Key
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# User Input
c1, c2, c3 = st.columns(3)
year = c1.text_input("Year", "2018")
make = c2.text_input("Make", "Tesla")
model = c3.text_input("Model", "Model 3")

if st.button("Generate Safety Report"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        # 1. Fetch Data
        url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
        response = requests.get(url)
        recalls = response.json().get('results', [])

        if not recalls:
            st.success("✅ No recalls found for this vehicle!")
        else:
            # 2. Display Table
            st.subheader("📋 Official Recall List")
            df = pd.DataFrame(recalls)[['Component', 'NHTSAActionNumber', 'ReportReceivedDate']]
            df.columns = ['Affected Part', 'NHTSA ID', 'Date Reported']
            st.dataframe(df, use_container_width=True)

            # 3. AI Analysis (Unified Summary)
            client = OpenAI(api_key=api_key)
            
            # Combine all recall descriptions into one text block for the AI
            all_recalls_text = "\n".join([f"- {r['Component']}: {r['Summary']}" for r in recalls])

            with st.spinner("AI is analyzing all safety risks..."):
                # THE UNIFIED PROMPT
                prompt = f"""
                You are a Senior Automotive Safety Inspector. 
                Below is a list of ALL active recalls for a {year} {make} {model}. 
                
                RECALL DATA:
                {all_recalls_text}

                TASK:
                1. Provide a single, cohesive summary (max 4 sentences) explaining the combined risk.
                2. Assign a RISK LEVEL: 'RED' if there is a risk of fire, crashes, or sudden steering/brake failure. 'YELLOW' for all other safety issues.
                
                OUTPUT FORMAT:
                RISK: [RED or YELLOW]
                SUMMARY: [Your summary here]
                """

                ai_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                content = ai_response.choices[0].message.content
                
                # Parse Risk and Summary
                risk_level = "RED" if "RISK: RED" in content.upper() else "YELLOW"
                summary_text = content.split("SUMMARY:")[-1].strip()

                # 4. Display Warning Sign
                st.subheader("⚠️ AI Safety Verdict")
                if risk_level == "RED":
                    st.markdown('<div class="flash-red">🚨 CRITICAL SAFETY RISK DETECTED - CONTACT DEALER IMMEDIATELY 🚨</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-yellow">⚠️ SAFETY WARNING - REPAIRS RECOMMENDED ⚠️</div>', unsafe_allow_html=True)
                
                st.info(summary_text)

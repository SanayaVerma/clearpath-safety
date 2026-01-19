import streamlit as st
import requests
from google import genai

# Page Setup
st.set_page_config(page_title="ClearPath Safety", page_icon="🚗")

st.title("🚗 ClearPath Safety (Gemini Edition)")

# 1. Setup API Key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# 2. User Input
c1, c2, c3 = st.columns(3)
year = c1.text_input("Year", value="2018")
make = c2.text_input("Make", value="Tesla")
model = c3.text_input("Model", value="Model 3")

if st.button("Check Safety Recalls"):
    if not api_key:
        st.error("Please provide a Gemini API Key.")
    else:
        # 3. Fetch Data from Data.gov
        api_url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
        
        with st.spinner("Connecting to Data.gov..."):
            response = requests.get(api_url)
            results = response.json().get('results', [])
            
            if not results:
                st.success("No active recalls found!")
            else:
                # 4. Gemini AI Analysis Layer
                client = genai.Client(api_key=api_key)
                
                for recall in results[:3]: # Analyze top 3
                    st.divider()
                    st.write(f"#### Component: {recall['Component']}")
                    
                    # Gemini Prompt
                    prompt = f"Explain this car recall simply for a non-expert: {recall['Summary']}"
                    
                    # Generate content using Gemini 1.5 Flash
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", 
                        contents=prompt
                    )
                    
                    st.info(f"**Gemini Safety Insight:**\n\n{response.text}")
import streamlit as st
import requests
from openai import OpenAI

# Page Setup
st.set_page_config(page_title="ClearPath Safety", page_icon="🚗", layout="centered")

# CSS to make it look modern
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .recall-card { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #ff4b4b; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 ClearPath Safety")
st.markdown("### Bridging the gap between complex government data and family safety.")

# 1. Sidebar - Setup API Key from Streamlit Secrets
# Note: When testing locally, you can replace this with a string: api_key = "your-key"
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.sidebar.warning("API Key not found in secrets. Please enter it below for testing:")
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# 2. User Input
with st.container():
    st.write("Enter vehicle details to check for active safety recalls:")
    c1, c2, c3 = st.columns(3)
    year = c1.text_input("Year", value="2018")
    make = c2.text_input("Make", value="Tesla")
    model = c3.text_input("Model", value="Model 3")

if st.button("Check Safety Recalls"):
    if not api_key:
        st.error("Please provide an API Key to enable AI analysis.")
    else:
        # 3. Fetch Live Data from NHTSA (Data.gov)
        api_url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
        
        with st.spinner("Searching National Highway Traffic Safety Administration database..."):
            try:
                response = requests.get(api_url)
                results = response.json().get('results', [])
                
                if not results:
                    st.success(f"✅ No active recalls found for the {year} {make} {model}.")
                else:
                    st.warning(f"⚠️ Found {len(results)} active recall(s).")
                    
                    # 4. AI Analysis Layer
                    client = OpenAI(api_key=api_key)
                    
                    for i, recall in enumerate(results):
                        with st.container():
                            st.markdown(f"---")
                            st.markdown(f"#### Recall #{i+1}: {recall['Component']}")
                            
                            # Show technical data in an expander
                            with st.expander("View Official Technical Summary"):
                                st.write(recall['Summary'])
                            
                            # AI "Translation"
                            prompt = f"Explain this car recall simply for a non-expert: {recall['Summary']}"
                            
                            ai_msg = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[{"role": "user", "content": prompt}]
                            )
                            
                            st.info(f"**AI Safety Advice:**\n\n{ai_msg.choices[0].message.content}")

            except Exception as e:
                st.error(f"Error connecting to Data.gov: {e}")

st.divider()
st.caption("Data provided by the NHTSA Recalls API via Data.gov. AI advice is for informational purposes only.")



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

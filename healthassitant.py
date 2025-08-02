import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# --- Load API Key ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Initialize Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI ---
st.set_page_config(page_title="🏥 Health Assistant", page_icon="💊")
st.title("💊  Health Assistant By Dua Habib")

st.markdown(
    "⚠️ **Disclaimer:** This assistant provides general health information only. "
    "Please consult a doctor for medical advice. "
    "It also provides diet tables and exercise tips."
)

# --- Chat History ---
if "chat" not in st.session_state:
    st.session_state.chat = []

# --- Language Selection ---
language = st.radio("Select Language / زبان منتخب کریں:", ["English", "اردو"])

# --- Multi-line Input (Textarea) ---
user_input = st.text_area("Enter your health-related question / اپنی صحت کا سوال لکھیں:", height=120)

# --- Submit Button ---
if st.button("Ask"):
    if user_input.strip() != "":
        # Detect Query Type & Heading
        heading = "🏥 Health Advice"
        if "exercise" in user_input.lower():
            heading = "💪 Exercise Tips"
        elif "diet" in user_input.lower() or "table" in user_input.lower():
            heading = "🥗 Diet Plan"

        # Add user query
        st.session_state.chat.append(("🧑 You", user_input))

        # System prompt
        system_prompt = f"""
        You are an AI Health Assistant. 
        1. If user gives symptoms (like 'fever + cough'), suggest possible causes, precautions, and when to see a doctor.  
        2. If user asks about exercise, give helpful workout tips.  
        3. If user asks about diet or diet table, provide a simple diet plan (Breakfast, Lunch, Dinner).  
        4. Always respond in {language}.  
        5. End your answer with a short health dua or positive note.  
        Example dua: 'May Allah bless you with good health. اللہ آپ کو صحت عطا فرمائے۔'  
        """

        # AI Response
        with st.spinner("Analyzing your question..."):
            response = model.generate_content(system_prompt + f"\n\nUser: {user_input}")
            answer = response.text

        # Store heading + answer
        st.session_state.chat.append((heading, answer))

# --- Display Chat History with Dynamic Headings ---
for role, msg in st.session_state.chat:
    if role.startswith("🧑"):
        st.markdown(f"**{role}:** {msg}")
    else:
        st.subheader(role)   # Dynamic heading (Health Advice, Diet Plan, Exercise Tips)
        st.write(msg)

# --- Footer / LinkedIn ---
st.markdown("---")
st.markdown(
    "👩‍💻 Developed by **Dua Habib**  \n"
    "[🔗 Connect with me on LinkedIn](https://www.linkedin.com/in/dua-habib-497557301/?originalSubdomain=pk)"
)

import streamlit as st
from openai import OpenAI

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Mørk bakgrunn med hvit skrift for lesbarhet
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { 
        border-radius: 12px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
        width: 100%;
    }
    .stSelectbox label { color: #FFB300 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering av poeng og meldinger
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- TOPP-RAD: Tittel og AI-Hjelper ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🏗️ Byggfagtreneren") #
    st.write(f"Poengsum: **{st.session_state.points}**")

with col2:
    with st.popover("🤖 AI-Hjelper"):
        st.write("### Spør Verksmesteren")
        user_prompt = st.chat_input("Hva lurer du på?")
        
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk på byggfaglige spørsmål for VG1-VG3 elever."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("API-nøkkel mangler i Secrets!")
            except Exception:
                st.error("Kunne ikke koble til AI-tjenesten.")

        for m in st.session_state.messages[-2:]:
            st.write(f"**Verksmesteren:** {m['content']}")

st.divider()

# --- NIVÅ-STYRING ---
if st.session_state.points < 100:
    n_key, status = "n1", "Lærling-spire 🌱"
elif st.session_state.points < 300:
    n_key, status = "n2", "F

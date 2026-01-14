import streamlit as st
from openai import OpenAI
import pandas as pd
import math

# 1. Konfigurasjon
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# Visuelt design (Mørkt tema og gule knapper)
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
        height: 3em;
    }
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering av tilstand
if 'startet' not in st.session_state:
    st.session_state.startet = False
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- FORSIDE (Vises før start) ---
if not st.session_state.startet:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    
    st.markdown("""
    ### Klar for å starte arbeidsdagen?
    Dette verktøyet hjelper deg med å bli trygg på byggeplassen. Vi skal gå gjennom:
    * **Verktøy og fagområder** for de 10 ulike retningene[cite: 10, 30].
    * **Praktisk matte** som måling, areal og vinkler[cite: 31, 34, 41].
    * **Sikkerhet og HMS** så alle kommer trygt hjem[cite: 26, 27].
    """)
    
    navn = st.text_input("Skriv navnet ditt her:", placeholder="Ditt navn...")
    
    if st.button("🚀 GÅ VIDERE TIL TRENING"):
        if navn:
            st.session_state.user_name = navn
            st.session_state.startet = True
            st.rerun()
        else:
            st.warning("Vennligst skriv inn navnet ditt for å fortsette.")
    st.stop()

# --- HOVEDAPP (Vises etter at man har trykket på knappen) ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Bruker: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}** [cite: 5]")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og pedagogisk[cite: 7]."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except:
                st.error("Kunne ikke koble til AI.")
        for m in st.session_state.messages[-2:]:
            st.write(f"**Verksmesteren:** {m['content']} [cite: 9]")

st.divider()

# Her fortsetter resten av koden din med tabs for info, matte og quiz...
tab_info, tab_matte, tab_quiz = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz"])

with tab_info:
    st.info("Velg et fagområde i menyen for å lære mer om verktøy og utdanning[cite: 30].")
    # (Legg inn din eksisterende data_db logikk her)

with tab_matte:
    st.header("📐 Praktisk matematikk")
    # (Legg inn din eksisterende matte-logikk her)

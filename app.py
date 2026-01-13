import streamlit as st
from openai import OpenAI
import pandas as pd

# 1. Design og Oppsett
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { border-radius: 12px; background-color: #FFB300; color: #000000 !important; font-weight: bold; width: 100%; }
    div[data-testid="stPopover"] > button { background-color: #FFB300 !important; color: #000000 !important; font-weight: bold !important; border: 2px solid #FFFFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialisering
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Navn:")
    if st.button("Start"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- TOPP-RAD ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Bruker: **{st.session_state.user_name}**")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        st.write("### Faglig hjelp")
        user_prompt = st.chat_input("Spør om noe...")
        
        if user_prompt:
            # DIAGNOSE:
            if "OPENAI_API_KEY" not in st.secrets:
                st.error("SYSTEMFEIL: Finner ikke 'OPENAI_API_KEY' i Streamlit Secrets. Sjekk Settings!")
            else:
                try:
                    # Prøver å koble til
                    test_key = st.secrets["OPENAI_API_KEY"]
                    client = OpenAI(api_key=test_key)
                    
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en norsk verksmester. Svar kort."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    # Viser den EKTE feilmeldingen fra OpenAI
                    st.error(f"OpenAI svarte med feil: {str(e)}")
                    st.info("Tips: Sjekk om du har penger (Credits) på OpenAI-kontoen din.")

        for m in st.session_state.messages[-3:]:
            st.write(f"🗨️ {m['content']}")

# (Resten av databasen og fanene forblir like som i forrige svar)
st.divider()
st.info("Sjekk Infokanalen eller ta Quizen under!")

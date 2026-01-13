import streamlit as st
from openai import OpenAI

# Konfigurasjon
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

# CSS for mørk bakgrunn og hvit skrift
st.markdown("""
    <style>
    .stApp { background-color: #121212; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    .stButton>button { 
        border-radius: 10px; 
        background-color: #FFB300; 
        color: #000000 !important; 
        font-weight: bold;
    }
    /* Gjør chat-vinduet litt mer kompakt */
    .stChatFloatingInputContainer { background-color: #222 !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialisering
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- TOPP-RAD: TITTEL OG AI-HJELPER SIDE OM SIDE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Poeng: **{st.session_state.points}**")

with col2:
    # En liten knapp for å åpne AI-chat i en "pop-over" (veldig moderne design)
    with st.popover("🤖 Spør AI-Hjelper"):
        st.write("Verksmesteren er klar!")
        
        # Enkel chat-funksjon inne i popoveren
        prompt = st.chat_input("Hva lurer du på?")
        if prompt:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            # Legg spørsmål til historikk
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Send til OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Du er en hjelpsom verksmester for VG1 og VG2 elever i byggfag. Svar kort og faglig korrekt på norsk."},
                    {"role": "user", "content": prompt}
                ]
            )
            ans = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ans})

        # Vis de siste meldingene i det lille vinduet
        for m in st.session_state.messages[-3:]:
            st.write(f"**{'Du' if m['role']=='user' else 'AI'}:** {m['content']}")

st.divider()

# --- PROGRAMOMRÅDER (Resten av appen) ---
temaer = ["Anleggsgartner", "Anleggsteknikk", "Betong og mur", "Klima, energi og miljøteknikk", 
          "Overflateteknikk", "Rørlegger", "Treteknikk", "Tømrer", "Arbeidsmiljø og dokumentasjon"]

valgt_tema = st.selectbox("Velg et fagområde:", temaer)

# Her følger quiz-logikken vi laget tidligere...
st.write(f"Du har valgt: **{valgt_tema}**")
st.info("Svar på spørsmålene under for å 'låse opp' neste nivå.")

# Eksempel på et spørsmål
if valgt_tema == "Tømrer":
    st.write("### Nivå 1: Hva er standard c/c på stendere?")
    svar = st.radio("Svar:", ["30 cm", "60 cm", "120 cm"], index=None)
    if st.button("Sjekk svar"):
        if svar == "60 cm":
            st.success("Riktig!")
            st.session_state.points += 10
            st.balloons()

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
    name = st.text_input("Ditt navn:")
    if st.button("Begynn"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- TOPP-RAD ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Elev: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}**")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        user_prompt = st.chat_input("Spør om fag...")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar kort som en norsk byggmester."}, {"role": "user", "content": user_prompt}]
                )
                ans = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                if "insufficient_quota" in str(e):
                    st.error("Verksmesteren er tom for kaffepenger (OpenAI Credits mangler).")
                    st.info("💡 Tips: Du finner svar på det meste i Infokanalen!")
                else:
                    st.error("Feil ved tilkobling til AI.")

        for m in st.session_state.messages[-2:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASEN (TEMA 1-10) ---
data_db = {
    "Anleggsgartner": {"beskrivelse": "Uterom og stein.", "verktoy": "Vater, snor.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hva brukes murersnor til?", ["Linjer", "Måle fukt"], "Linjer")},
    "Anleggsteknikk": {"beskrivelse": "Vei og tunnel.", "verktoy": "Gravemaskin.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hva er påbudt i grøft?", ["Hjelm", "Joggesko"], "Hjelm")},
    "Betong og mur": {"beskrivelse": "Grunnmur og stein.", "verktoy": "Blandemaskin.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hvorfor armere?", ["Strekkfasthet", "Pynt"], "Strekkfasthet")},
    "Klima, energi og miljøteknikk": {"beskrivelse": "Ventilasjon og ENØK.", "verktoy": "Måleutstyr.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hvorfor isolere?", ["Spare energi", "Pynt"], "Spare energi")},
    "Overflateteknikk": {"beskrivelse": "Maling og gulv.", "verktoy": "Pensel, sparkel.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hva gjøres først?", ["Vaske", "Male"], "Vaske")},
    "Rørlegger": {"beskrivelse": "Vann og varme.", "verktoy": "Rørkutter.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Hva gjør vannlås?", ["Stoppe lukt", "Øke trykk"], "Stoppe lukt")},
    "Treteknikk": {"beskrivelse": "Industriell produksjon.", "verktoy": "CNC, sag.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Tresort til reisverk?", ["Gran", "Eik"], "Gran")},
    "Tømrer": {"beskrivelse": "Bygge hus i tre.", "verktoy": "Hammer, drill.", "utdanning": "Vg1 -> Vg2 -> Lærling", "quiz": ("Standard c/c?", ["60 cm", "100 cm"], "60 cm")},
    "Arbeidsmiljø og dokumentasjon": {"beskrivelse": "HMS og SJA.", "verktoy": "Sjekklister.", "utdanning": "Gjennomgående.", "quiz": ("Hva er SJA?", ["Sikker jobb-analyse", "Snekker-avtale"], "Sikker jobb-analyse")},
    "Yrkesfaglig fordypning": {"beskrivelse": "Praksis i bedrift.", "verktoy": "Varierer.", "utdanning": "Vg1 og Vg2.", "quiz": ("Viktigst i praksis?", ["Møte presis", "Kunne alt"], "Møte presis")}
}

# --- FANER ---
tab_info, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    selected = st.selectbox("Velg fagområde:", list(data_db.keys()))
    f = data_db[selected]
    st.subheader(f"📍 {selected}")
    c1, c2 = st.columns(2)
    with c1: st.write(f"**Beskrivelse:** {f['beskrivelse']}")
    with c2: st.write(f"**Verktøy:** {f['verktoy']}")
    st.info(f"**Utdanning:** {f['utdanning']}")

with tab_quiz:
    valgt_q = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_sel")
    spm, valg, svar = data_db[valgt_q]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk"):
        if res == svar:
            st.success("Riktig! +20 poeng"); st.session_state.points += 20; st.balloons(); st.rerun()
        else: st.error("Feil!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Demo"], "Poeng": [st.session_state.points, 400]}))

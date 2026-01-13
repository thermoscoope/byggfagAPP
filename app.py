import streamlit as st
from openai import OpenAI
import pandas as pd
import math

# 1. Konfigurasjon og Visuelt Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="centered")

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
    div[data-testid="stPopover"] > button {
        background-color: #FFB300 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #FFFFFF !important;
    }
    .stSelectbox label { color: #FFB300 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Velkommen til Byggfagtreneren")
    name = st.text_input("Skriv inn navnet ditt for å starte:")
    if st.button("Start Trening"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- TOPP-RAD ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Bruker: **{st.session_state.user_name}** | Poeng: **{st.session_state.points}**")

with col2:
    with st.popover("👷 Spør verksmesteren", use_container_width=True):
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar kort som en norsk byggmester."}, {"role": "user", "content": user_prompt}]
                )
                ans = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except:
                st.error("AI-hjelper er utilgjengelig.")
        for m in st.session_state.messages[-2:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE FOR TEMAER ---
data_db = {
    "Anleggsgartner": {"beskrivelse": "Uterom og stein.", "verktoy": "Vater, snor.", "utdanning": "Vg1 -> Vg2", "quiz": ("Hva brukes murersnor til?", ["Linjer", "Måle fukt"], "Linjer")},
    "Tømrer": {"beskrivelse": "Bygge hus i tre.", "verktoy": "Hammer, drill.", "utdanning": "Vg1 -> Vg2", "quiz": ("Standard c/c?", ["60 cm", "100 cm"], "60 cm")},
    "Betong og mur": {"beskrivelse": "Grunnmur og stein.", "verktoy": "Blandemaskin.", "utdanning": "Vg1 -> Vg2", "quiz": ("Hvorfor armere?", ["Strekkfasthet", "Pynt"], "Strekkfasthet")},
    "Arbeidsmiljø og dokumentasjon": {"beskrivelse": "HMS og SJA.", "verktoy": "Sjekklister.", "utdanning": "Gjennomgående.", "quiz": ("Hva er SJA?", ["Sikker jobb-analyse", "Snekker-avtale"], "Sikker jobb-analyse")}
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    valgt_info = st.selectbox("Velg fag:", list(data_db.keys()), key="info_select")
    if valgt_info in data_db:
        f = data_db[valgt_info]
        st.subheader(f"📍 {valgt_info}")
        st.write(f"**Arbeidsområde:** {f['beskrivelse']}")
        st.write(f"**Verktøy:** {f['verktoy']}")

with tab_matte:
    st.header("📐 Praktisk matematikk")
    underkategori = st.radio("Velg område:", ["Omkrets & Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler & Pytagoras"], horizontal=True)
    
    if underkategori == "Omkrets & Areal":
        st.subheader("📏 Omkrets og Areal")
        st.write("**Omkrets:** Summen av alle sider (L+B+L+B). Brukes til lister og gjerder.")
        st.write("**Areal:** Lengde x Bredde. Brukes til parkett, maling og belegningsstein.")
        
        st.markdown("---")
        st.write("**Oppgave:** En vegg er 4m bred og 2,5m høy. Hvor mange m² skal males?")
        svar_areal = st.radio("Velg svar:", ["6,5 m²", "10 m²", "12 m²"], index=None)
        if st.button("Sjekk Areal"):
            if svar_areal == "10 m²":
                st.success("Riktig! 4 * 2,5 = 10m²"); st.session_state.points += 5
            else: st.error("Prøv igjen.")

    elif underkategori == "Vg2: Vinkler & Pytagoras":
        st.subheader("📐 Vinkler og Pytagoras (3-4-5 metoden)")
        st.write("For å sjekke om et hjørne er nøyaktig 90 grader (i vinkel), bruker vi Pytagoras' læresetning:")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("I praksis betyr dette: Hvis du måler 30cm ut på en vegg og 40cm ut på den andre, skal diagonalen mellom punktene være nøyaktig 50cm.")
        
        
        st.markdown("---")
        st.write("**Oppgave:** Du skal sjekke om et hjørne på en stor platting er i vinkel. Du måler 3 meter på den ene siden og 4 meter på den andre. Hva skal diagonalen være for at vinkelen er 90 grader?")
        svar_pyt = st.radio("Velg svar:", ["5 meter", "6 meter", "7 meter"], index=None)
        if st.button("Sjekk Vinkel"):
            if svar_pyt == "5 meter":
                st.success("Helt korrekt! Dette er den klassiske 3-4-5 regelen."); st.session_state.points += 15
                st.balloons()
            else: st.error("Feil. Husk: 3² + 4² = 9 + 16 = 25. Kvadratroten av 25 er 5.")

    elif underkategori == "Prosent & Svinn":
        st.subheader("📈 Prosent og Svinn")
        st.write("Når du bestiller materialer, må du legge til litt ekstra (svinn) fordi noe kappes bort.")
        st.write("**Oppgave:** Du trenger egentlig 100 meter panel, men læreren sier du må legge til 10% i svinn. Hvor mye må du bestille?")
        svar_svinn = st.radio("Velg svar:", ["101 meter", "110 meter", "120 meter"], index=None)
        if st.button("Sjekk Svinn"):
            if svar_svinn == "110 meter":
                st.success("Riktig!"); st.session_state.points += 5
            else: st.error("Feil. 10% av 100 er 10.")

    elif underkategori == "Målestokk":
        st.subheader("🗺️ Målestokk")
        st.write("Hvor lang er en vegg i virkeligheten hvis den er 10cm på en tegning i 1:50?")
        svar_mal = st.radio("Svar:", ["5 meter", "50 cm", "2 meter"], index=None)
        if st.button("Sjekk Målestokk"):
            if svar_mal == "5 meter":
                st.success("Riktig! 10cm * 50 = 500cm = 5m"); st.session_state.points += 10

with tab_quiz:
    st.header("🎮 Quiz-trening")
    valgt_tema = st.selectbox("Velg tema:", list(data_db.keys()), key="quiz_select")
    spm, valg, svar = data_db[valgt_tema]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Ditt svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer"], "Poeng": [st.session_state.points, 500]}))

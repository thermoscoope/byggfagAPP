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
    name = st.text_input("Navn på elev:")
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
                    messages=[{"role": "system", "content": "Svar som en erfaren byggmester. Kort og pedagogisk."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except:
                st.error("AI-hjelper utilgjengelig.")
        for m in st.session_state.messages[-2:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE FOR ALLE 10 TEMAER ---
data_db = {
    "Anleggsgartner": {
        "info": "🌱 **Hva gjør man?** Bygger og vedlikeholder uterom. **Verktøy:** Vater, steinkutter, gravemaskin. **Utdanning:** Vg1 Bygg -> Vg2 Anleggsgartner. **Motivasjon:** Lag varige spor i naturen!",
        "quiz": ("Hva brukes en murersnor til?", ["Lage rette linjer", "Måle fukt"], "Lage rette linjer")
    },
    "Anleggsteknikk": {
        "info": "🚜 **Hva gjør man?** Veibygging og tunnelarbeid. **Verktøy:** Gravemaskin, dumper. **Utdanning:** Vg1 -> Vg2 Anleggsteknikk. **Motivasjon:** Flytt fjell og bygg landet!",
        "quiz": ("Hva er påbudt i grøft?", ["Hjelm og vernesko", "Hørselsvern"], "Hjelm og vernesko")
    },
    "Betong og mur": {
        "info": "🧱 **Hva gjør man?** Konstruksjon i betong og stein. **Verktøy:** Forskaling, laser. **Utdanning:** Vg1 -> Vg2 Betong og mur. **Motivasjon:** Bygg fundamentet som står evig!",
        "quiz": ("Hvorfor armere betong?", ["Øke strekkfasthet", "For fargen"], "Øke strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "info": "🌡️ **Hva gjør man?** Ventilasjon og energisparing. **Verktøy:** Måleinstrumenter. **Utdanning:** Vg1 -> Vg2 KEM. **Motivasjon:** Bli en helt i det grønne skiftet!",
        "quiz": ("Hvorfor isolerer vi bygg?", ["Spare energi", "For tyngden"], "Spare energi")
    },
    "Overflateteknikk": {
        "info": "🎨 **Hva gjør man?** Maling og gulvlegging. **Verktøy:** Sparkel, malerulle. **Utdanning:** Vg1 -> Vg2 Overflate. **Motivasjon:** Gi byggene sjel og farge!",
        "quiz": ("Hva gjøres før maling?", ["Vaske og fjerne støv", "Male rett på"], "Vaske og fjerne støv")
    },
    "Rørlegger": {
        "info": "🚿 **Hva gjør man?** Vann og varme. **Verktøy:** Rørkutter, trykkpumpe. **Utdanning:** Vg1 -> Vg2 Rørlegger. **Motivasjon:** Viktig arbeid for folkehelse og komfort!",
        "quiz": ("Hva gjør en vannlås?", ["Hindre kloakklukt", "Rense vann"], "Hindre kloakklukt")
    },
    "Treteknikk": {
        "info": "🏭 **Hva gjør man?** Industriell treproduksjon. **Verktøy:** CNC-maskiner. **Utdanning:** Vg1 -> Vg2 Treteknikk. **Motivasjon:** Kombiner naturmateriale med høyteknologi!",
        "quiz": ("Hvilken tresort brukes mest?", ["Gran", "Eik"], "Gran")
    },
    "Tømrer": {
        "info": "🏠 **Hva gjør man?** Bygge hus i tre. **Verktøy:** Hammer, sag, laser. **Utdanning:** Vg1 -> Vg2 Tømrer. **Motivasjon:** Se et hjem reise seg fra dine egne hender!",
        "quiz": ("Hva er standard c/c?", ["60 cm", "100 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "info": "🛡️ **Hva gjør man?** HMS og sikkerhet. **Verktøy:** SJA, sjekklister. **Utdanning:** Del av alle fag. **Motivasjon:** Sørg for at alle kommer trygt hjem!",
        "quiz": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Hele Min Snekker"], "Helse, Miljø og Sikkerhet")
    },
    "Yrkesfaglig fordypning": {
        "info": "🤝 **Hva gjør man?** Praksis i bedrift. **Verktøy:** Holdninger og interesse. **Utdanning:** Vg1 og Vg2. **Motivasjon:** Din sjanse til å få drømmejobben!",
        "quiz": ("Viktigst i praksis?", ["Oppmøte og interesse", "Ny mobil"], "Oppmøte og interesse")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fagområde:", list(data_db.keys()))
    st.subheader(f"📍 {sel_fag}")
    st.write(data_db[sel_fag]["info"])

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Volum", "Prosent & Svinn", "Målestokk", "Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets – Lengden rundt")
        st.write("Omkrets er den totale lengden av ytterkantene. Nyttig for lister og gjerder.")
        st.latex(r"O = S_1 + S_2 + S_3 + S_4")
        st.write("**Oppgave:** Et rom er 5m x 4m. Hvor mange meter list trenger du?")
        ans1 = st.radio("Svar:", ["9m", "18m", "20m"], index=None, key="m1")
        if st.button("Sjekk Omkrets"):
            if ans1 == "18m":
                st.success("Riktig! (5+4+5+4)"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal – Flateberegning")
        st.write("Areal (m²) er Lengde x Bredde. Brukes til gulv, gips og maling.")
        

[Image of the formula for the area of a rectangle]

        st.latex(r"A = L \times B")
        st.write("**Oppgave:** Du skal legge gips i et tak på 3m x 4m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["7m²", "12m²", "10m²"], index=None, key="m2")
        if st.button("Sjekk Areal"):
            if ans2 == "12m²":
                st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Volum":
        st.write("### 🧊 Volum – Kubikk")
        st.write("Volum (m³) er Lengde x Bredde x Høyde. Brukes for å bestille betong.")
        

[Image of the volume of a rectangular prism]

        st.latex(r"V = L \times B \times H")
        st.write("**Oppgave:** En såle er 5m lang, 2m bred og 0,2m høy. Hvor mye betong?")
        ans_v = st.radio("Svar:", ["1m³", "2m³", "7m³"], index=None, key="mv")
        if st.button("Sjekk Volum"):
            if ans_v == "2m³":
                st.success("Riktig! 5 * 2 * 0,2 = 2"); st.session_state.points += 10

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("Vi legger til 10% svinn ved å gange behovet med 1,10.")
        st.write("**Oppgave:** Du trenger 60m panel. Hvor mye bestiller du med 10% svinn?")
        ans3 = st.radio("Svar:", ["66m", "60,1m"], index=None, key="m3")
        if st.button("Sjekk Svinn"):
            if ans3 == "66m":
                st.success("Riktig!"); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("1:50 betyr at virkeligheten er 50 ganger større enn tegningen.")
        st.write("**Oppgave:** 10cm på tegning (1:50). Hvor langt er det i virkeligheten?")
        ans4 = st.radio("Svar:", ["5 meter", "50 cm"], index=None, key="m4")
        if st.button("Sjekk Målestokk"):
            if ans4 == "5 meter":
                st.success("Riktig! 10 * 50 = 500cm = 5m"); st.session_state.points += 10

    elif m_kat == "Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("For å sjekke 90 grader: Hvis katetene er 3 og 4, er diagonalen 5.")
        
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave:** Sidene i et hjørne er 60cm og 80cm. Hva er diagonalen?")
        ans5 = st.radio("Svar:", ["100cm", "140cm"], index=None, key="m5")
        if st.button("Sjekk Vinkel"):
            if ans5 == "100cm":
                st.success("Riktig!"); st.session_state.points += 15; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()
        else:
            st.error("Feil svar!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Demo"], "Poeng": [st.session_state.points, 400]}))

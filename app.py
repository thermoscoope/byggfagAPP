import streamlit as st

# --- 1. KONFIGURASJON OG MOBIL-OPTIMALISERT DESIGN ---
st.set_page_config(
    page_title="Byggfag Pro", 
    page_icon="🏗️", 
    layout="wide", # Bruker hele bredden på mobil
    initial_sidebar_state="collapsed" # Skjuler menyen som standard på små skjermer
)

# Avansert CSS for mobilvennlighet (Mobile First)
st.markdown("""
    <style>
    /* Hovedbakgrunn */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    /* Justering for mobilskjermer */
    @media (max-width: 640px) {
        .main-title {
            font-size: 24px !important;
        }
        .category-card {
            padding: 15px !important;
        }
    }

    /* Tilpasset Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 40, 0.95) !important;
        backdrop-filter: blur(10px);
    }

    /* Styling av menyelementer - HVIT TEKST */
    .stRadio > div {
        background-color: transparent !important;
    }
    
    .stRadio label {
        color: #ffffff !important;
        padding: 12px 15px !important; /* Større touch-flate */
        border-radius: 10px !important;
        margin-bottom: 8px !important;
        font-size: 16px;
    }

    /* Valgt menyvalg */
    .stRadio label[data-selected="true"] {
        background: linear-gradient(90deg, #8a2be2 0%, #da70d6 100%) !important;
        color: #ffffff !important;
    }

    /* Glassmorphism Kort - Responsiv */
    .category-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        width: 100%;
    }

    /* Store knapper for tommel-trykking */
    div.stButton > button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
    }

    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SPØRSMÅLSBANK (Samme som før) ---
quiz_data = {
    "Tømrer": [
        {"q": "Hva er standard c/c avstand på stendere i en bærevegg?", "a": ["300 mm", "600 mm", "900 mm"], "correct": "600 mm"},
        {"q": "Hva betyr 'SJA'?", "a": ["Sikker jobb-analyse", "Snekker-jern-avstand", "Samarbeid"], "correct": "Sikker jobb-analyse"},
        {"q": "Hvilket verktøy brukes for å sjekke lodd og vater?", "a": ["Vater", "Tommestokk", "Krittsnor"], "correct": "Vater"},
        {"q": "Hvor høyt kan et stillas være før det kreves opplæring for montering?", "a": ["2 meter", "5 meter", "10 meter"], "correct": "5 meter"},
        {"q": "Hvilken farge har ofte bokser for farlig avfall?", "a": ["Rød", "Blå", "Grønn"], "correct": "Rød"},
        {"q": "Hva betyr målestokk 1:50?", "a": ["1 cm = 50 cm", "50 cm = 1 cm", "1 m = 50 m"], "correct": "1 cm = 50 cm"},
        {"q": "Hvilken side av vindsperren skal vende ut?", "a": ["Den med trykk", "Den glatte", "Ingen betydning"], "correct": "Den med trykk"},
        {"q": "Hvorfor bruker vi lekter på tak?", "a": ["Feste takstein/lufting", "Gjøre taket tyngre", "Pynt"], "correct": "Feste takstein/lufting"},
        {"q": "Hvilket materiale regnes som mest bærekraftig i Norge?", "a": ["Tre", "Stål", "Betong"], "correct": "Tre"},
        {"q": "Hva brukes et sikkerhetsdatablad til?", "a": ["Info om kjemikalier", "Bruksanvisning", "Lønnsoversikt"], "correct": "Info om kjemikalier"},
        {"q": "Hva er hensikten med kildesortering?", "a": ["Miljø og økonomi", "Kun rydding", "Tvang"], "correct": "Miljø og økonomi"},
        {"q": "Hva kjennetegner god byggeskikk i værutsatte strøk?", "a": ["Gode takutstikk", "Flate tak", "Store vinduer"], "correct": "Gode takutstikk"},
        {"q": "Hva er en svill?", "a": ["Bunnen i en vegg", "Toppen av et vindu", "Spiker"], "correct": "Bunnen i en vegg"},
        {"q": "Hva brukes en vinkel til?", "a": ["Sjekke 90 grader", "Måle lengde", "Slå spiker"], "correct": "Sjekke 90 grader"},
        {"q": "Hva dokumenterer du i loggboka?", "a": ["Eget arbeid og HMS", "Været", "Hva andre gjør"], "correct": "Eget arbeid og HMS"}
    ],
    # ... Legg inn de andre fagene her på samme måte som i forrige koding ...
}

# --- 3. MENY-NAVIGASJON ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Byggfagtreneren</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; font-size:12px; font-weight:bold;'>HOVEDMENY</p>", unsafe_allow_html=True)
    side = st.radio("", ["🏠 Dashboard", "🎯 Kunnskapstest", "📝 Loggbok"], label_visibility="collapsed")
    
    st.markdown("<br><p style='color:white; font-size:12px; font-weight:bold;'>PROGRAMOMRÅDE</p>", unsafe_allow_html=True)
    fag_valg = st.radio("", list(quiz_data.keys()), label_visibility="collapsed")

# --- 4. HOVEDINNHOLD (Mobil-optimalisert) ---
if side == "🏠 Dashboard":
    st.markdown(f"<h1 class='main-title'>Hei, Lærling! 👋</h1>", unsafe_allow_html=True)
    
    # Kolonner som stabler seg på mobil
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"<div class='category-card'><h4>{fag_valg}</h4><p>Nivå: VG1</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='category-card'><h4>Dagens mål</h4><p>Fullfør HMS-quiz</p></div>", unsafe_allow_html=True)

elif side == "🎯 Kunnskapstest":
    st.markdown(f"<h2 class='main-title'>Test: {fag_valg}</h2>", unsafe_allow_html=True)
    
    if 'q_idx' not in st.session_state or st.session_state.get('current_fag') != fag_valg:
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.current_fag = fag_valg

    if st.session_state.q_idx < 15:
        curr = quiz_data[fag_valg][st.session_state.q_idx]
        st.progress(st.session_state.q_idx / 15)
        
        st.markdown(f"<div class='category-card'><b>Spørsmål {st.session_state.q_idx + 1}</b><br>{curr['q']}</div>", unsafe_allow_html=True)
        valg = st.radio("Svar:", curr['a'], key=f"q_{st.session_state.q_idx}")
        
        if st.button("NESTE"):
            if valg == curr['correct']:
                st.session_state.score += 1
            st.session_state.q_idx += 1
            st.rerun()
    else:
        st.markdown(f"<div class='category-card'><h2>Ferdig!</h2><h1>{st.session_state.score}/15</h1></div>", unsafe_allow_html=True)
        if st.button("PRØV IGJEN"):
            st.session_state.q_idx = 0
            st.rerun()

elif side == "📝 Loggbok":
    st.markdown("<h2 class='main-title'>Loggføring</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='category-card'>Registrer arbeid i {fag_valg}</div>", unsafe_allow_html=True)
    st.camera_input("Ta bilde av utført arbeid") # Åpner kameraet direkte på mobil
    st.text_area("Hva har du gjort i dag?")
    st.button("SEND INN")


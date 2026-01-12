import streamlit as st

# --- 1. KONFIGURASJON OG AVANSERT CSS ---
st.set_page_config(page_title="Byggfag Pro", page_icon="🏗️", layout="wide")

# CSS for å gjenskape Finora-menyen og mørkt design
st.markdown("""
    <style>
    /* Hovedbakgrunn */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    /* Tilpasset Sidebar som Finora-malen */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 40, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        min-width: 250px !important;
        max-width: 250px !important;
    }

    /* Styling av menyelementer (radio-buttons i sidebar) */
    .stRadio > div {
        background-color: transparent !important;
        padding: 0px !important;
    }
    
    .stRadio label {
        background-color: transparent;
        color: #a0a0c0 !important;
        padding: 10px 15px !important;
        border-radius: 10px !important;
        margin-bottom: 5px !important;
        transition: 0.3s;
        display: flex;
        align-items: center;
    }

    /* Høydepunkt på valgt menyvalg (Lilla gradient som i Finora) */
    .stRadio label[data-selected="true"] {
        background: linear-gradient(90deg, #8a2be2 0%, #da70d6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
    }

    /* Glassmorphism Kort */
    .category-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Titler */
    .main-title {
        color: #ffffff;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 30px;
    }
    
    /* Skjul standard Streamlit header */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIKK FOR MENY (FINORA STIL) ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:20px;'>Finora Bygg</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#6c757d; font-size:12px; margin-bottom:5px;'>MAIN</p>", unsafe_allow_html=True)
    side = st.radio("", ["🏠 Dashboard", "🤖 AI Veileder"], label_visibility="collapsed")
    
    st.markdown("<br><p style='color:#6c757d; font-size:12px; margin-bottom:5px;'>UTDANNING</p>", unsafe_allow_html=True)
    fag_valg = st.radio("", [
        "🏗️ Tømrer", 
        "🚜 Anleggsteknikk", 
        "🔧 Rørlegger", 
        "🧱 Betong og mur", 
        "🎨 Overflateteknikk",
        "🌱 Klima & Miljø"
    ], label_visibility="collapsed")
    
    st.markdown("<br><p style='color:#6c757d; font-size:12px; margin-bottom:5px;'>VERKTØY</p>", unsafe_allow_html=True)
    verktoy = st.radio("", ["🎯 Kunnskapstest", "📝 Loggbok", "⚙️ Innstillinger"], label_visibility="collapsed")

# --- 3. INNHOLD BASERT PÅ VALG ---
if side == "🏠 Dashboard":
    st.markdown(f"<h1 class='main-title'>Dashboard - {fag_valg}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='category-card'>
            <h4>Fremdrift i {fag_valg.split(' ')[1]}</h4>
            <p style='color:#a0a0c0;'>Fullfør dagens kompetansemål</p>
            <div style='background:#2d2d44; border-radius:10px; height:10px; width:100%; margin-top:15px;'>
                <div style='background:linear-gradient(90deg, #8a2be2, #da70d6); width:65%; height:10px; border-radius:10px;'></div>
            </div>
            <p style='text-align:right; font-size:12px; margin-top:5px;'>65% Fullført</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='category-card'>
            <h4>Siste Aktivitet</h4>
            <p style='color:#a0a0c0;'>HMS-sjekkliste utført i dag</p>
            <span style='background:rgba(0,255,0,0.1); color:#00ff00; padding:4px 10px; border-radius:20px; font-size:12px;'>Godkjent</span>
        </div>
        """, unsafe_allow_html=True)

# Seksjon for HMS basert på læreplanen din
st.markdown("<h3 style='margin-top:40px;'>Kritiske Kompetansemål</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div class='category-card'>
    <ul>
        <li>Vurdere risiko og utføre forebyggende tiltak</li>
        <li>Bruke arbeidsteknikker som forebygger helseskader</li>
        <li>Planlegge, gjennomføre og dokumentere eget arbeid</li>
    </ul>
</div>
""", unsafe_allow_html=True)

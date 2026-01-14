import streamlit as st
from openai import OpenAI
import pandas as pd
import math

# 1. Konfigurasjon - Layout "wide" er ofte brukt i moderne dashbord
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="wide")

# 2. Base44-inspirert CSS (Mørkeblå toner, avrundede kort, profesjonell skrift)
st.markdown("""
    <style>
    /* Bakgrunn og skrifttype */
    .stApp { background-color: #0B0E14; }
    * { font-family: 'Inter', 'Segoe UI', sans-serif; }

    /* Sidemeny (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #11141D;
        border-right: 1px solid #1F2937;
    }

    /* Kort-design for innhold */
    .stMarkdown div[data-testid="stMarkdownContainer"] p, .stAlert, div.row-widget.stButton {
        color: #D1D5DB;
    }
    
    /* Overskrifter */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Knapper (Base44 stil: Blå/Indigo) */
    .stButton>button { 
        border-radius: 8px; 
        background-color: #4F46E5; 
        color: #FFFFFF !important; 
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Radio-knapper og Selectbox */
    .stSelectbox label, .stRadio label { color: #9CA3AF !important; }
    
    /* Styling av faner (hvis de brukes) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #11141D;
        border-radius: 8px 8px 0 0;
        color: #9CA3AF;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisering
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.title("🏗️ Byggfagtreneren")
        st.write("Logg inn for å starte din faglige reise.")
        name = st.text_input("Ditt navn:")
        if st.button("Logg inn"):
            if name:
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# --- SIDEMENY (Navigasjon) ---
with st.sidebar:
    st.title("🏗️ Treneren")
    nav_valg = st.radio("MENY", ["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])
    st.divider()
    st.write(f"Elev: **{st.session_state.user_name}**")
    st.write(f"Poeng: **{st.session_state.points}**")
    
    # AI-hjelper i bunnen av sidemeny
    with st.expander("👷 Spør verksmesteren"):
        prompt = st.chat_input("Hva lurer du på?")
        if prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar kort som byggmester."}, {"role": "user", "content": prompt}]
                )
                st.session_state.messages.append(res.choices[0].message.content)
            except: st.error("AI utilgjengelig")
        for m in st.session_state.messages[-1:]: st.write(f"🗨️ {m}")

# --- DATABASE (Viktigste programfag) ---
data_db = {
    "Tømrer": {
        "beskrivelse": "🏠 **Tømrerfaget:** Som tømrer bygger du hus i tre fra grunnen av. Du jobber med alt fra reisverk og tak til finsnekring inne.",
        "verktoy": "Hammer, kappsag, laser, drill, vinkel.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Tømrer -> Lærling.",
        "videre": "🎓 Mesterbrev eller byggeleder.",
        "motivasjon": "Liker du å skape noe varig med hendene? Tømrerfaget gir deg stolthet i hvert bygg!",
        "quiz": ("Hva er standard c/c på stendere i Norge?", ["60 cm", "40 cm"], "60 cm")
    },
    "Anleggsteknikk": {
        "beskrivelse": "🚜 **Anleggsteknikk:** Du opererer de største maskinene som finnes og bygger veier, tunneler og jernbane.",
        "verktoy": "Gravemaskin, hjullaster, dumper, GPS-utstyr.",
        "utdanning": "📜 Vg1 Bygg -> Vg2 Anleggsteknikk -> Lærling.",
        "videre": "🎓 Maskinentreprenørskolen eller fagskole.",
        "motivasjon": "Bli med på å flytte fjell! Her får du ansvar for maskiner verdt millioner.",
        "quiz": ("Hva gjør en dumper?", ["Flytter masser", "Maler striper"], "Flytter masser")
    }
}

# --- HOVEDINNHOLD ---
if nav_valg == "📚 Infokanal":
    st.header("Informasjonskanal")
    sel = st.selectbox("Velg retning:", list(data_db.keys()))
    f = data_db[sel]
    
    st.markdown(f"### {sel}")
    st.info(f["beskrivelse"])
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🛠️ Verktøy")
        st.write(f["verktoy"])
    with c2:
        st.markdown("#### 🎓 Utdanningsløp")
        st.write(f["utdanning"])
    
    st.success(f"**🚀 Videreutdanning:** {f['videre']}")
    st.info(f"💡 **Motivasjon:** {f['motivasjon']}")

elif nav_valg == "📐 Praktisk matte":
    st.header("Praktisk matematikk")
    m_kat = st.selectbox("Velg tema:", ["Omkrets", "Areal", "Volum", "Prosent & Svinn", "Målestokk", "Vinkler"])
    
    if m_kat == "Areal":
        st.subheader("⬛ Arealberegning")
        st.write("Areal forteller oss hvor stor en flate er ($m^2$). Brukes til parkett, gips og maling.")
        st.latex(r"Areal = L \cdot B")
        st.write("**Oppgave:** Et tak er 6 meter langt og 3 meter bredt. Hvor mange $m^2$ gipsplater trenger du?")
        ans = st.radio("Velg svar:", ["9", "18", "20"], index=None)
        if st.button("Sjekk svar"):
            if ans == "18": st.success("Riktig! 6 * 3 = 18."); st.session_state.points += 5
            else: st.error("Feil. Prøv igjen.")

    elif m_kat == "Volum":
        st.subheader("🧊 Volumberegning")
        st.write("Volum brukes for å finne ut hvor mye en form rommer ($m^3$), for eksempel betong.")
        st.latex(r"Volum = L \cdot B \cdot H")
        st.write("**Oppgave:** En forskaling er 2m lang, 2m bred og 0,5m høy. Hvor mye betong går med?")
        ans_v = st.radio("Svar:", ["2 m³", "4 m³", "1 m³"], index=None)
        if st.button("Sjekk Volum"):
            if ans_v == "2 m³": st.success("Riktig! 2 * 2 * 0,5 = 2."); st.session_state.points += 10

    elif m_kat == "Vinkler":
        st.subheader("📐 Vinkler og Pytagoras")
        st.write("Bruk 3-4-5 metoden for å sjekke om et hjørne er 90 grader.")
        st.latex(r"a^2 + b^2 = c^2")
        st.write("**Oppgave:** Sidene er 3 meter og 4 meter. Hva må diagonalen være for at det skal være vinkel?")
        ans_pyt = st.radio("Svar:", ["5 meter", "6 meter"], index=None)
        if st.button("Sjekk Vinkel"):
            if ans_pyt == "5 meter": st.success("Perfekt! Dette er '3-4-5-regelen'."); st.session_state.points += 15

elif nav_valg == "🎮 Quiz":
    st.header("Dagens utfordring")
    q_tema = st.selectbox("Velg tema:", list(data_db.keys()))
    spm, valg, svar = data_db[q_tema]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Ditt valg:", valg, index=None)
    if st.button("Lever svar"):
        if res == svar:
            st.success("Riktig svar! +20 poeng")
            st.session_state.points += 20
            st.balloons()
        else: st.error("Feil. Sjekk infokanalen og prøv igjen.")

elif nav_valg == "🏆 Leaderboard":
    st.header("Toppliste")
    leader_df = pd.DataFrame({"Elev": [st.session_state.user_name, "Lærer-demo"], "Poeng": [st.session_state.points, 450]})
    st.table(leader_df.sort_values(by="Poeng", ascending=False))

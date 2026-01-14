import streamlit as st
from openai import OpenAI
import pandas as pd
import math

# 1. Konfigurasjon og e-Board Design
st.set_page_config(page_title="Byggfagtreneren", page_icon="🏗️", layout="wide")

# CSS for å etterligne e-Board (Mørkt, profesjonelt og rent)
st.markdown("""
    <style>
    /* Hovedbakgrunn */
    .stApp { background-color: #0E1117; }
    
    /* Tekstfarger */
    h1, h2, h3, p, span, label { color: #E0E0E0 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Sidemeny-styling */
    [data-testid="stSidebar"] {
        background-color: #1A1C24;
        border-right: 1px solid #30363D;
    }
    
    /* Knapper som ligner e-Board */
    .stButton>button { 
        border-radius: 4px; 
        background-color: #238636; /* e-Board grønn suksess-farge */
        color: #FFFFFF !important; 
        font-weight: 500;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2EA043;
        border: none;
    }

    /* Info-bokser */
    .stAlert {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisering
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# --- INNLOGGING ---
if not st.session_state.user_name:
    st.title("🏗️ Byggfagtreneren - Logg inn")
    name = st.text_input("Navn på elev:")
    if st.button("Logg inn"):
        if name:
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- SIDEMENY (NAVIGASJON) ---
with st.sidebar:
    st.image("https://www.vilbli.no/img/vilbli-logo.svg", width=150) # Eksempel logo
    st.title("Meny")
    side_valg = st.radio("Gå til:", ["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])
    
    st.divider()
    st.write(f"👤 **{st.session_state.user_name}**")
    st.write(f"🏆 Poeng: {st.session_state.points}")
    
    # AI-hjelperen flyttet til sidemenyen (som en chat-widget)
    with st.expander("👷 Spør verksmesteren"):
        u_input = st.chat_input("Hva lurer du på?")
        if u_input:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar kort som byggmester."}, {"role": "user", "content": u_input}]
                )
                st.session_state.messages.append(res.choices[0].message.content)
            except: st.error("AI utilgjengelig")
        for m in st.session_state.messages[-1:]:
            st.write(f"💬 {m}")

# --- DATABASE (Forkortet for eksempel) ---
data_db = {
    "Tømrer": {
        "info": "🏠 **Tømrerfaget:** Oppføring av trebygninger. Bindingsverk, tak og interiør.",
        "verktoy": "Hammer, kappsag, laser, drill.",
        "videre": "Mesterbrev, Fagskole.",
        "motivasjon": "Bli med på å bygge fremtidens hjem!",
        "quiz": ("Hva er c/c 60?", ["Avstand mellom stendere", "Høyde på dør"], "Avstand mellom stendere")
    },
    "Anleggsteknikk": {
        "info": "🚜 **Anleggsteknikk:** Veibygging og tunnelarbeid med store maskiner.",
        "verktoy": "Gravemaskin, dumper, GPS.",
        "videre": "Maskinførerskolen.",
        "motivasjon": "Flytt fjell og skap infrastruktur!",
        "quiz": ("Hva gjør en dumper?", ["Flytter masser", "Maler striper"], "Flytter masser")
    }
}

# --- HOVEDINNHOLD BASERT PÅ MENYVALG ---
if side_valg == "📚 Infokanal":
    st.header("Informasjonskanal")
    sel = st.selectbox("Velg programområde:", list(data_db.keys()))
    f = data_db[sel]
    st.markdown(f"### {sel}")
    st.info(f["info"])
    c1, c2 = st.columns(2)
    with c1: st.write("**🛠️ Verktøy:** " + f["verktoy"])
    with c2: st.write("**🎓 Videre:** " + f["videre"])
    st.warning("💡 " + f["motivasjon"])

elif side_valg == "📐 Praktisk matte":
    st.header("Praktisk matematikk")
    m_kat = st.selectbox("Velg emne:", ["Omkrets", "Areal", "Volum", "Prosent & Svinn", "Målestokk", "Vinkler"])
    
    if m_kat == "Areal":
        st.write("### ⬛ Arealberegning")
        st.write("Areal forteller hvor stor en flate er. Formel: Lengde x Bredde.")
        st.latex(r"A = L \cdot B")
        

[Image of area calculation for a rectangle]

        st.write("**Oppgave:** Et gulv er 4m x 3m. Hvor mange m²?")
        ans = st.radio("Svar:", ["7", "12", "10"], index=None)
        if st.button("Sjekk"):
            if ans == "12": st.success("Riktig!"); st.session_state.points += 5
            else: st.error("Feil")

    elif m_kat == "Volum":
        st.write("### 🧊 Volumberegning")
        st.write("Volum brukes for å finne ut hvor mye en form rommer, f.eks. betong.")
        st.latex(r"V = L \cdot B \cdot H")
        

[Image of volume calculation for a rectangular prism]

        st.write("**Oppgave:** En form er 2m x 2m x 0,5m. Hvor mye betong?")
        ans_v = st.radio("Svar:", ["2 m³", "4 m³", "1 m³"], index=None)
        if st.button("Sjekk Volum"):
            if ans_v == "2 m³": st.success("Riktig!"); st.session_state.points += 10

elif side_valg == "🎮 Quiz":
    st.header("Dagens Quiz")
    q_fag = st.selectbox("Tema:", list(data_db.keys()))
    spm, valg, svar = data_db[q_fag]["quiz"]
    st.write(f"### {spm}")
    r = st.radio("Velg:", valg, index=None)
    if st.button("Svar"):
        if r == svar: st.success("Riktig!"); st.session_state.points += 20; st.balloons()

elif side_valg == "🏆 Leaderboard":
    st.header("Leaderboard")
    st.table(pd.DataFrame({"Elev": [st.session_state.user_name, "Demo"], "Poeng": [st.session_state.points, 450]}))

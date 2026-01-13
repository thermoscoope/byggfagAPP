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
if 'points' not in st.session_state: st.session_state.points = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'user_name' not in st.session_state: st.session_state.user_name = ""

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
        st.write("### Spør om alt innen byggfag")
        user_prompt = st.chat_input("Hva lurer du på?")
        if user_prompt:
            try:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": "Svar som en norsk byggmester. Kort og pedagogisk."}, {"role": "user", "content": user_prompt}]
                )
                st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            except: st.error("AI-hjelper er utilgjengelig.")
        for m in st.session_state.messages[-2:]: st.write(f"🗨️ {m['content']}")

st.divider()

# --- DATABASE (INFO & QUIZ) ---
data_db = {
    "Anleggsgartner": {
        "info": "🌱 **Hva lærer man?** Bygging og vedlikehold av uterom. Bruk av planter, stein, betong og treverk.\n\n🧱 **Viktige punkter:** Grunnarbeid, drenering, beleggingsstein og murer.",
        "quiz": ("Hva er en sentral del av arbeidet som anleggsgartner?", ["Overvannshåndtering", "Sikre sikringsskap"], "Overvannshåndtering")
    },
    "Anleggsteknikk": {
        "info": "🚜 **Hva lærer man?** Betjening av store maskiner for veibygging, tunneler og utgraving.\n\n💥 **Viktige punkter:** Maskinføring, sprengning og grunnarbeid.",
        "quiz": ("Hvilken maskin flytter mest masser?", ["Dumper", "Hammer"], "Dumper")
    },
    "Betong og mur": {
        "info": "🧱 **Hva lærer man?** Konstruksjon i betong, tegl og stein. Fra grunnmur til store bygg.\n\n🏗️ **Viktige punkter:** Forskaling, armering og muring.",
        "quiz": ("Hva gjør armering?", ["Øker strekkfasthet", "Gjør den hvit"], "Øker strekkfasthet")
    },
    "Klima, energi og miljøteknikk": {
        "info": "🌡️ **Hva lærer man?** Tekniske systemer for ventilasjon, varme og energiøkonomisering.\n\n❄️ **Viktige punkter:** Inneklima, varmepumper og isolering.",
        "quiz": ("Hva er hovedformålet med ventilasjon?", ["God luftkvalitet", "Mindre lys"], "God luftkvalitet")
    },
    "Overflateteknikk": {
        "info": "🎨 **Hva lærer man?** Beskyttelse og dekor av bygg. Maling, tapet og gulvlegging.\n\n🖌️ **Viktige punkter:** Grunnarbeid, sparkling og materialkunnskap.",
        "quiz": ("Hvorfor sparkle skjøter?", ["Få slett overflate", "Låse døra"], "Få slett overflate")
    },
    "Rørlegger": {
        "info": "🚿 **Hva lærer man?** Vann, varme og avløp i alle typer bygg.\n\n🛠️ **Viktige punkter:** Sanitærutstyr, rør-i-rør og varmeanlegg.",
        "quiz": ("Hva gjør en vannlås?", ["Hindrer kloakklukt", "Renser vann"], "Hindrer kloakklukt")
    },
    "Treteknikk": {
        "info": "🏭 **Hva lærer man?** Industriell produksjon med tre som råstoff.\n\n⚙️ **Viktige punkter:** CNC-maskiner, produksjon av vinduer, dører og takstoler.",
        "quiz": ("Hva er limtre?", ["Limte trelag for styrke", "Papir"], "Limte trelag for styrke")
    },
    "Tømrer": {
        "info": "🔨 **Hva lærer man?** Oppføring av trebygninger fra reisverk til ferdig hus.\n\n🏠 **Viktige punkter:** Bindingsverk, tak, vinduer og dører.",
        "quiz": ("Hva er standard c/c på stendere?", ["60 cm", "20 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "info": "🛡️ **Hva lærer man?** Sikkerhet på byggeplassen og lovverk.\n\n📝 **Viktige punkter:** HMS, SJA og risikovurdering.",
        "quiz": ("Hva står SJA for?", ["Sikker jobb-analyse", "Snekker-avtale"], "Sikker jobb-analyse")
    },
    "Yrkesfaglig fordypning": {
        "info": "🤝 **Hva lærer man?** Praksis i bedrift og lære rutiner i yrkeslivet.\n\n📈 **Viktige punkter:** Holdninger, punktlighet og samarbeid.",
        "quiz": ("Viktigst i praksis?", ["Oppmøte og interesse", "Ny mobil"], "Oppmøte og interesse")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fag:", list(data_db.keys()))
    st.subheader(f"📍 {sel_fag}")
    st.markdown(data_db[sel_fag]["info"])

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets (Lengden rundt)")
        st.write("Bruk dette når du skal beregne lister langs gulvet. Formel: Legg sammen alle sidene.")
        st.latex(r"L + B + L + B")
        st.write("**Oppgave:** Et rom er 5m x 4m. Hvor mange meter list trenger du?")
        ans1 = st.radio("Svar:", ["9m", "18m", "20m"], index=None, key="m1")
        if st.button("Sjekk 1"):
            if ans1 == "18m": st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal (Overflaten)")
        st.write("Bruk dette for gulv og maling. Formel: Lengde ganger Bredde.")
        st.latex(r"L \times B = m^2")
        [Image of area calculation for a rectangle]
        st.write("**Oppgave:** Du skal legge gulv i en bod på 2,5m x 3m. Hvor mange m²?")
        ans2 = st.radio("Svar:", ["5,5 m²", "7,5 m²", "10 m²"], index=None, key="m2")
        if st.button("Sjekk 2"):
            if ans2 == "7,5 m²": st.success("Riktig!"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("Legg til 10% svinn ved å gange med 1,10.")
        st.write("**Oppgave:** Du trenger 80m kledning. Hvor mye bestiller du med 10% svinn?")
        ans3 = st.radio("Svar:", ["88m", "80,1m"], index=None, key="m3")
        if st.button("Sjekk 3"):
            if ans3 == "88m": st.success("Riktig!"); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("Diagonalen må være 5 hvis sidene er 3 og 4.")
        st.latex(r"a^2 + b^2 = c^2")
        [Image of the 3-4-5 rule for checking right angles in construction]
        st.write("**Oppgave:** Sider er 30cm og 40cm. Hva er diagonalen i vinkel?")
        ans5 = st.radio("Svar:", ["50cm", "70cm"], index=None, key="m5")
        if st.button("Sjekk 5"):
            if ans5 == "50cm": st.success("Vinkelen er 90 grader!"); st.session_state.points += 20; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys

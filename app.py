import streamlit as st
from openai import OpenAI

# 1. Konfigurasjon og Design
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
    /* Stil for radio-knapper så de synes godt */
    .stRadio [data-testid="stMarkdownContainer"] { color: white !important; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Initialisering av data
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- TOPP-RAD: Tittel og AI ved siden av hverandre ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🏗️ Byggfagtreneren")
    st.write(f"Poengsum: **{st.session_state.points}**")

with col2:
    with st.popover("🤖 Spør AI-Hjelper"):
        st.write("### Verksmesteren")
        user_prompt = st.chat_input("Spør om byggfag...")
        
        if user_prompt:
            try:
                # Sjekker om nøkkelen finnes før vi kaller AI
                if "OPENAI_API_KEY" in st.secrets:
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du er en erfaren norsk verksmester. Svar kort og enkelt på byggfaglige spørsmål for VG1-VG3 elever."},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    ans = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    st.error("API-nøkkel mangler i Settings -> Secrets!")
            except Exception as e:
                st.error(f"AI-feil: Legg inn API-nøkkel i Streamlit Secrets for å aktivere.")

        for m in st.session_state.messages[-3:]:
            st.write(f"🗨️ {m['content']}")

st.divider()

# --- LOGIKK FOR NIVÅ ---
if st.session_state.points < 100:
    n_key = "n1"
    status = "Lærling-spire 🌱"
elif st.session_state.points < 300:
    n_key = "n2"
    status = "Fagarbeider 🛠️"
else:
    n_key = "n3"
    status = "Mester 🏆"

st.write(f"Din status: **{status}**")

# --- SPØRSMÅL-DATABASE ---
quiz_db = {
    "Tømrer": {
        "n1": ("Hva er standard c/c på stendere?", ["30 cm", "60 cm", "120 cm"], "60 cm"),
        "n2": ("Hva slags spiker brukes utendørs?", ["Varmforzinket", "Blank", "Kobber"], "Varmforzinket"),
        "n3": ("Hva er viktigst ved dimensjonering av sperrer?", ["Snølast og spennvidde", "Fargen på treet", "Prisen"], "Snølast og spennvidde")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "n1": ("Hva står HMS for?", ["Helse, Miljø og Sikkerhet", "Husk Mye Sagmugg", "Hjelp Med Snekring"], "Helse, Miljø og Sikkerhet"),

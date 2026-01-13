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

# --- UTVIDET DATABASE (INFO FRA VILBLI.NO & QUIZ) ---
data_db = {
    "Anleggsgartner": {
        "info": "🌱 **Hva lærer man?** Du lærer å bygge, drifte og vedlikeholde uterom. Det innebærer arbeid med både 'levende' materialer som planter og 'harde' materialer som stein og betong.\n\n🧱 **Viktige punkter:** Grunnarbeid, overvannshåndtering, legging av belegningsstein, muring og vedlikehold av grøntanlegg.\n\n👷 **Arbeidsplass:** Entreprenørbedrifter eller kommunale etater.",
        "quiz": ("Hva er en sentral oppgave for en anleggsgartner?", ["Overvannshåndtering og drenering", "Montere sikringsskap"], "Overvannshåndtering og drenering")
    },
    "Anleggsteknikk": {
        "info": "🚜 **Hva lærer man?** Drift og vedlikehold av anleggsmaskiner. Du lærer om veibygging, jernbane, tunneler og utgraving av tomter.\n\n💥 **Viktige punkter:** Maskinføring, sprengningsarbeid, masseflytting og stikningsarbeid.\n\n🏗️ **Arbeidsplass:** Store anleggsentreprenører eller pukkverk.",
        "quiz": ("Hvilken maskin brukes til komprimering av masser?", ["Valse eller vibrasjonsplate", "Motorsag"], "Valse eller vibrasjonsplate")
    },
    "Betong og mur": {
        "info": "🏢 **Hva lærer man?** Å bygge solide konstruksjoner i betong, tegl, blokker og naturstein. Du lærer å lese tegninger og sette opp forskaling.\n\n🏗️ **Viktige punkter:** Armering, støping, muring av fasader og piper, og flislegging.\n\n🧱 **Arbeidsplass:** Murmesterfirmaer eller betongentreprenører.",
        "quiz": ("Hvorfor legger man armeringsstål i betong?", ["For å øke strekkfastheten", "For at den skal tørke raskere"], "For å øke strekkfastheten")
    },
    "Klima, energi og miljøteknikk": {
        "info": "🌡️ **Hva lærer man?** Tekniske systemer som sikrer godt inneklima og lavt energiforbruk. Inkluderer blikkenslagerarbeid og ventilasjon.\n\n❄️ **Viktige punkter:** Varme- og kjølesystemer, ENØK, isolering og fasadearbeid.\n\n💡 **Arbeidsplass:** Ventilasjonsfirmaer eller blikkenslagerverksteder.",
        "quiz": ("Hva er hovedformålet med ventilasjon i bygg?", ["Sikre god luftkvalitet og fjerne fukt", "Gjøre rommet lysere"], "Sikre god luftkvalitet og fjerne fukt")
    },
    "Overflateteknikk": {
        "info": "🎨 **Hva lærer man?** Beskyttelse og dekor av overflater. Du lærer om materialer, farger og ulike påføringsteknikker.\n\n🖌️ **Viktige punkter:** Sparkling, sliping, maling, tapetsering og legging av gulvbelegg.\n\n🏠 **Arbeidsplass:** Malerfirmaer eller gulvleggingsbedrifter.",
        "quiz": ("Hva er viktigste grunn til å sparkle skjøter på gipsplater?", ["For å få en slett og jevn overflate", "For å lime platene sammen"], "For å få en slett og jevn overflate")
    },
    "Rørlegger": {
        "info": "🚿 **Hva lærer man?** Installasjon og vedlikehold av vann-, avløps- og varmeanlegg. Du lærer om sanitærutstyr og sprinkelanlegg.\n\n🛠️ **Viktige punkter:** Rør-i-rør systemer, lodding, sveising og trykktesting.\n\n💧 **Arbeidsplass:** Rørleggerbedrifter eller industrianlegg.",
        "quiz": ("Hva gjør en vannlås i et avløpssystem?", ["Hindrer kloakklukt fra å komme inn i rommet", "Renser vannet"], "Hindrer kloakklukt fra å komme inn i rommet")
    },
    "Treteknikk": {
        "info": "🏭 **Hva lærer man?** Industriell produksjon av treprodukter. Du lærer å betjene avanserte maskiner for å lage bygningsdeler.\n\n⚙️ **Viktige punkter:** CNC-teknologi, limtreproduksjon, høvling og overflatebehandling av tre.\n\n🌲 **Arbeidsplass:** Sagbruk, høvlerier eller vindusfabrikker.",
        "quiz": ("Hva kjennetegner 'limtre'?", ["Laminerte trelag som gir stor bæreevne", "Trevirke som er malt hvitt"], "Laminerte trelag som gir stor bæreevne")
    },
    "Tømrer": {
        "info": "🔨 **Hva lærer man?** Oppføring og rehabilitering av trebygninger. Du lærer å bygge alt fra reisverk til ferdig interiør.\n\n🏠 **Viktige punkter:** Bindingsverk, takkonstruksjoner, montering av vinduer/dører og isolering.\n\n📐 **Arbeidsplass:** Tømrerfirmaer eller ferdighusprodusenter.",
        "quiz": ("Hva er standard avstand (c/c) mellom stendere i en vegg?", ["60 cm", "100 cm"], "60 cm")
    },
    "Arbeidsmiljø og dokumentasjon": {
        "info": "🛡️ **Hva lærer man?** Lovverk og rutiner for HMS. Du lærer å dokumentere eget arbeid og vurdere risiko.\n\n📝 **Viktige punkter:** SJA (Sikker jobb-analyse), bruk av verneutstyr og kvalitetssikring.\n\n⚠️ **Viktig:** Dette er grunnlaget for alt arbeid i bygg og anlegg.",
        "quiz": ("Når skal en SJA (Sikker Jobb-analyse) utføres?", ["Før en risikofylt arbeidsoperasjon starter", "Etter at uhellet har skjedd"], "Før en risikofylt arbeidsoperasjon starter")
    },
    "Yrkesfaglig fordypning": {
        "info": "🤝 **Hva lærer man?** Du får prøve deg i arbeidslivet og blir kjent med ulike yrker og bedrifter.\n\n📈 **Viktige punkter:** Samarbeid, punktlighet, HMS i praksis og faglig stolthet.\n\n🏢 **Mål:** Å finne ut hvilket fag man vil ta svennebrev i og sikre seg læreplass.",
        "quiz": ("Hva er lurt å fokusere på for å få læreplass i YFF-perioden?", ["Vise gode holdninger og møte presis", "Ha det dyreste verktøyet"], "Vise gode holdninger og møte presis")
    }
}

# --- FANER ---
tab_info, tab_matte, tab_quiz, tab_leader = st.tabs(["📚 Infokanal", "📐 Praktisk matte", "🎮 Quiz", "🏆 Leaderboard"])

with tab_info:
    st.header("Informasjon om programfagene")
    sel_fag = st.selectbox("Velg fagområde:", list(data_db.keys()))
    st.subheader(f"📍 {sel_fag}")
    st.markdown(data_db[sel_fag]["info"])

with tab_matte:
    st.header("📐 Praktisk matematikk")
    m_kat = st.radio("Velg emne:", ["Omkrets", "Areal", "Prosent & Svinn", "Målestokk", "Vg2: Vinkler & Pytagoras"], horizontal=True)
    
    if m_kat == "Omkrets":
        st.write("### 📏 Omkrets (Lengden rundt)")
        st.write("Omkrets er den totale lengden av alle ytterkantene til en figur. Brukes ofte til å beregne lister, gjerder eller grunnmursplast.")
        st.latex(r"Formel: L + B + L + B")
        st.write("**Oppgave:** Et rom er 5 meter langt og 4 meter bredt. Hvor mange meter gulvlist trenger du?")
        ans1 = st.radio("Svar:", ["9 meter", "18 meter", "20 meter"], index=None, key="m1")
        if st.button("Sjekk 1"):
            if ans1 == "18 meter": st.success("Riktig! (5 + 4 + 5 + 4)"); st.session_state.points += 5

    elif m_kat == "Areal":
        st.write("### ⬛ Areal (Overflaten)")
        st.write("Areal forteller hvor stor en flate er. Vi bruker dette når vi skal kjøpe inn parkett, gipsplater eller maling.")
        st.latex(r"Formel: Lengde \times Bredde = m^2")
        
        st.write("**Oppgave:** Du skal legge gipsplater i et tak som er 3 meter bredt og 4 meter langt. Hvor mange m² gips trenger du?")
        ans2 = st.radio("Svar:", ["7 m²", "12 m²", "15 m²"], index=None, key="m2")
        if st.button("Sjekk 2"):
            if ans2 == "12 m²": st.success("Helt rett! 3 * 4 = 12 m²"); st.session_state.points += 5

    elif m_kat == "Prosent & Svinn":
        st.write("### 📈 Prosent og Svinn")
        st.write("På byggeplassen bestiller vi alltid litt ekstra materialer fordi noe kappes bort. Dette kalles svinn. Vanligvis legger vi til 10%.")
        st.write("**Oppgave:** Du trenger 50 meter kledning, men må legge til 10% svinn. Hvor mye bestiller du?")
        ans3 = st.radio("Svar:", ["55 meter", "51 meter"], index=None, key="m3")
        if st.button("Sjekk 3"):
            if ans3 == "55 meter": st.success("Riktig! 10% av 50 er 5. 50 + 5 = 55."); st.session_state.points += 10

    elif m_kat == "Målestokk":
        st.write("### 🗺️ Målestokk")
        st.write("Målestokk 1:50 betyr at virkeligheten er 50 ganger større enn på papiret. 1 cm på tegningen = 50 cm i virkeligheten.")
        st.write("**Oppgave:** På en tegning i 1:100 måler du en vegg til 7 cm. Hvor lang er den i virkeligheten?")
        ans4 = st.radio("Svar:", ["70 cm", "7 meter"], index=None, key="m4")
        if st.button("Sjekk 4"):
            if ans4 == "7 meter": st.success("Riktig! 7cm * 100 = 700cm = 7m."); st.session_state.points += 10

    elif m_kat == "Vg2: Vinkler & Pytagoras":
        st.write("### 📐 Vinkler (3-4-5 regelen)")
        st.write("For å sjekke om et hjørne er nøyaktig 90 grader, bruker vi Pytagoras. Hvis de korte sidene er 3 og 4, må den lange diagonalen være nøyaktig 5.")
        st.latex(r"a^2 + b^2 = c^2")
        
        st.write("**Oppgave:** Du måler 60 cm på en vegg og 80 cm på den andre. Hva skal diagonalen være hvis det er vinkel?")
        ans5 = st.radio("Svar:", ["100 cm", "140 cm"], index=None, key="m5")
        if st.button("Sjekk 5"):
            if ans5 == "100 cm": st.success("Perfekt! (30*2, 40*2, 50*2)."); st.session_state.points += 20; st.balloons()

with tab_quiz:
    q_sel = st.selectbox("Velg quiz:", list(data_db.keys()), key="q_box")
    spm, valg, svar = data_db[q_sel]["quiz"]
    st.write(f"### {spm}")
    res = st.radio("Ditt svar:", valg, index=None)
    if st.button("Sjekk Quiz"):
        if res == svar:
            st.success("Riktig!"); st.session_state.points += 20; st.balloons(); st.rerun()
        else: st.error("Feil svar, prøv igjen!")

with tab_leader:
    st.table(pd.DataFrame({"Navn": [st.session_state.user_name, "Lærer"], "Poeng": [st.session_state.points, 400]}))

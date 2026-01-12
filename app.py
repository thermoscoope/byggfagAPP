import streamlit as st
import requests
from streamlit_lottie import st_lottie

# --- 1. KONFIGURASJON OG DESIGN ---
st.set_page_config(page_title="Byggfag Mester", page_icon="🏗️", layout="centered")

# CSS for å lage et lekent, bygg-relatert design
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .main-title { color: #2C3E50; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .category-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #FFCC00;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    div.stButton > button {
        background-color: #FFCC00;
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid #333;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #333;
        color: #FFCC00;
    }
    </style>
    """, unsafe_allow_html=True)

# Funksjon for animasjoner
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_builder = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_i9mxcD.json")

# --- 2. KOMPLETT SPØRSMÅLSBANK (Alle 5 programmer à 15 spørsmål) ---
quiz_data = {
    "Tømrer": [
        {"q": "Hva er standard c/c avstand på stendere i en bærevegg?", "a": ["300 mm", "600 mm", "900 mm"], "correct": "600 mm"},
        {"q": "Hva betyr 'SJA'?", "a": ["Sikker jobb-analyse", "Snekker-jern-avstand", "Samarbeid i arbeidslivet"], "correct": "Sikker jobb-analyse"},
        {"q": "Hvilket verktøy brukes for å sjekke lodd og vater?", "a": ["Vater", "Tommestokk", "Krittsnor"], "correct": "Vater"},
        {"q": "Hvor høyt kan et stillas være før det kreves spesifisert opplæring for montering?", "a": ["2 meter", "5 meter", "9 meter"], "correct": "5 meter"},
        {"q": "Hvilken farge har ofte bokser for farlig avfall?", "a": ["Rød", "Blå", "Grønn"], "correct": "Rød"},
        {"q": "Hva betyr målestokk 1:50?", "a": ["1 cm = 50 cm", "50 cm = 1 cm", "1 m = 50 m"], "correct": "1 cm = 50 cm"},
        {"q": "Hvilken side av vindsperren skal vende ut?", "a": ["Den med trykk", "Den glatte", "Ingen betydning"], "correct": "Den med trykk"},
        {"q": "Hvorfor bruker vi lekter på tak?", "a": ["Feste takstein/lufting", "Gjøre taket tyngre", "Pynt"], "correct": "Feste takstein/lufting"},
        {"q": "Hvilket materiale er mest bærekraftig?", "a": ["Tre", "Stål", "Betong"], "correct": "Tre"},
        {"q": "Hva brukes et sikkerhetsdatablad til?", "a": ["Info om kjemikalier", "Bruksanvisning hammer", "Lønnsoversikt"], "correct": "Info om kjemikalier"},
        {"q": "Hva er hensikten med kildesortering?", "a": ["Miljø og økonomi", "Kun rydding", "Lovpålagt tvang"], "correct": "Miljø og økonomi"},
        {"q": "Hva kjennetegner god byggeskikk i værutsatte strøk?", "a": ["Gode takutstikk", "Flate tak", "Store vinduer uten list"], "correct": "Gode takutstikk"},
        {"q": "Hva er en svill?", "a": ["Bunnen i en veggkonstruksjon", "Toppen av et vindu", "En type spiker"], "correct": "Bunnen i en veggkonstruksjon"},
        {"q": "Hva brukes en vinkel til?", "a": ["Sjekke 90 graders hjørner", "Måle lengde", "Slå inn spiker"], "correct": "Sjekke 90 graders hjørner"},
        {"q": "Hva dokumenterer du i loggboka?", "a": ["Eget arbeid og HMS", "Været", "Hva andre gjør"], "correct": "Eget arbeid og HMS"}
    ],
    "Anleggsteknikk": [
        {"q": "Hva må sjekkes før graving nær kabler?", "a": ["Ledningskart/kabelpåviser", "Værmelding", "Jordfarge"], "correct": "Ledningskart/kabelpåviser"},
        {"q": "Hva gjøres før man forlater en maskin?", "a": ["Senke utstyr til bakken", "La motoren gå", "Løfte skuffa"], "correct": "Senke utstyr til bakken"},
        {"q": "Risiko i usikret grøft over 2 meter?", "a": ["Raseulykker", "Ingen risiko", "Støv"], "correct": "Raseulykker"},
        {"q": "Signal for 'Stopp'?", "a": ["Begge armer ut", "Vinke", "En hånd i lomma"], "correct": "Begge armer ut"},
        {"q": "Hvorfor daglig kontroll av maskin?", "a": ["Forebygge svikt/ulykker", "Pynt", "Tidsfordriv"], "correct": "Forebygge svikt/ulykker"},
        {"q": "Hva er komprimering?", "a": ["Pakke masser med vals", "Vanne jord", "Flytte stein"], "correct": "Pakke masser med vals"},
        {"q": "Hva brukes fiberduk til?", "a": ["Separasjon av masselag", "Varme", "Pynt"], "correct": "Separasjon av masselag"},
        {"q": "Hva er stikking?", "a": ["Markere høyder/linjer", "Fjerne gress", "Rydde skog"], "correct": "Markere høyder/linjer"},
        {"q": "Hvilken masse drenerer best?", "a": ["Pukk", "Leire", "Silt"], "correct": "Pukk"},
        {"q": "Hva brukes rotasjonslaser til?", "a": ["Kontrollere høyder", "Kappe rør", "Lys"], "correct": "Kontrollere høyder"},
        {"q": "Hva betyr WLL på en stropp?", "a": ["Maks lasteevne", "Lengde", "Produsent"], "correct": "Maks lasteevne"},
        {"q": "Søl av hydraulikkolje?", "a": ["Absorbere/rapportere", "Dekk med grus", "Helle vann"], "correct": "Absorbere/rapportere"},
        {"q": "Hva betyr det å anhuke?", "a": ["Feste last til kran/maskin", "Grave", "Parkere"], "correct": "Feste last til kran/maskin"},
        {"q": "Klimaendringers effekt på anlegg?", "a": ["Mer overvannshåndtering", "Ingen", "Mindre graving"], "correct": "Mer overvannshåndtering"},
        {"q": "Hvor leveres farlig avfall fra maskin?", "a": ["Godkjent mottak", "Restavfall", "Grave ned"], "correct": "Godkjent mottak"}
    ],
    "Rørlegger": [
        {"q": "Krav for varme arbeider?", "a": ["Sertifikat og brannvakt", "Kun lighter", "Ingenting"], "correct": "Sertifikat og brannvakt"},
        {"q": "Tid for brannvakt etter arbeid?", "a": ["60 minutter", "5 minutter", "Ingen tid"], "correct": "60 minutter"},
        {"q": "Kjemikalier i øynene?", "a": ["Skylle med vann/SDB", "Gni", "Vente"], "correct": "Skylle med vann/SDB"},
        {"q": "Hensikt med trykktesting?", "a": ["Sjekke tetthet", "Sprekke rør", "Rense"], "correct": "Sjekke tetthet"},
        {"q": "Hvorfor ergonomi?", "a": ["Forebygge skader", "Jobbe raskere", "Pynt"], "correct": "Forebygge skader"},
        {"q": "Hva brukes rørtang til?", "a": ["Holde/skru rør", "Hamre", "Måle"], "correct": "Holde/skru rør"},
        {"q": "Hva betyr 'fall' på rør?", "a": ["Skråning for avrenning", "Ødelagt rør", "Miste rør"], "correct": "Skråning for avrenning"},
        {"q": "Hva gjør isolasjon på kaldtvannsrør?", "a": ["Hindre kondens/frost", "Pynt", "Støy"], "correct": "Hindre kondens/frost"},
        {"q": "Symbol for stoppekran?", "a": ["Ventiltrekant", "Sirkel med kryss", "Firkant"], "correct": "Ventiltrekant"},
        {"q": "Hva er lin og salve?", "a": ["Gjengetetting", "Sårbehandling", "Smøring"], "correct": "Gjengetetting"},
        {"q": "Fordel med rør-i-rør?", "a": ["Utskiftbart/vannskadesikkert", "Billigere plast", "Tøffere"], "correct": "Utskiftbart/vannskadesikkert"},
        {"q": "Hvorfor vannmåler?", "a": ["Måle forbruk/lekkasje", "Begrense trykk", "Lovpålagt"], "correct": "Måle forbruk/lekkasje"},
        {"q": "Håndtering av gamle kobberrør?", "a": ["Gjenvinning", "Restavfall", "Grave ned"], "correct": "Gjenvinning"},
        {"q": "Hva brukes til rensing av rør?", "a": ["Base/Syre", "Kun vann", "Olje"], "correct": "Base/Syre"},
        {"q": "Viktigst ved planlegging av bad?", "a": ["Sluk og vannplassering", "Farge", "Speil"], "correct": "Sluk og vannplassering"}
    ],
    "Betong og mur": [
        {"q": "Ingredienser i betong?", "a": ["Sement, vann, tilslag", "Gips", "Leire"], "correct": "Sement, vann, tilslag"},
        {"q": "Hvorfor armering?", "a": ["Tåle strekkrefter", "Tørke fort", "Lettere"], "correct": "Tåle strekkrefter"},
        {"q": "Hva betyr vibrering av betong?", "a": ["Fjerne luftbobler", "Gjøre flytende", "Farge"], "correct": "Fjerne luftbobler"},
        {"q": "Funksjon til muremørtel?", "a": ["Lime stein", "Pynt", "Hindre fukt"], "correct": "Lime stein"},
        {"q": "Etterbehandling av betong?", "a": ["Holde fuktig", "Blåse tørr", "Ingenting"], "correct": "Holde fuktig"},
        {"q": "Verktøy for mørtel?", "a": ["Mureskje", "Vinkelsliper", "Hammer"], "correct": "Mureskje"},
        {"q": "Hva er et forband?", "a": ["Mønster for styrke", "Bandasje", "Sementtype"], "correct": "Mønster for styrke"},
        {"q": "Maks fallhøyde for betong?", "a": ["1,5 meter", "5 meter", "10 meter"], "correct": "1,5 meter"},
        {"q": "Verneutstyr ved sementblanding?", "a": ["Støvmaske/hansker", "Hørselvern", "Ingenting"], "correct": "Støvmaske/hansker"},
        {"q": "Hva er forskaling?", "a": ["Form for betong", "Hvilepause", "Verktøykasse"], "correct": "Form for betong"},
        {"q": "Hva er herdetid?", "a": ["Tid til full styrke", "Blandingstid", "Lunsj"], "correct": "Tid til full styrke"},
        {"q": "Stein i fundament?", "a": ["Leca/Betongblokk", "Tegl", "Skifer"], "correct": "Leca/Betongblokk"},
        {"q": "For mye vann i betongen?", "a": ["Svakere styrke", "Sterkere", "Ingenting"], "correct": "Svakere styrke"},
        {"q": "Hva er eksponeringsklasse?", "a": ["Miljøkrav (f.eks salt)", "Seere", "Pris"], "correct": "Miljøkrav (f.eks salt)"},
        {"q": "Hva måles med slumptest?", "a": ["Konsistens", "Mengde", "Temp"], "correct": "Konsistens"}
    ],
    "Overflateteknikk": [
        {"q": "Grunnarbeid før maling?", "a": ["Vask og mattsliping", "Male direkte", "Kun vann"], "correct": "Vask og mattsliping"},
        {"q": "Tapet på ujevn vegg?", "a": ["Ujevnheter synes", "Retter veggen", "Ingen effekt"], "correct": "Ujevnheter synes"},
        {"q": "Funksjon til grunning?", "a": ["Heft og metting", "Farge", "Billigere"], "correct": "Heft og metting"},
        {"q": "Hva er diffusjonsåpen?", "a": ["Puster (slipper damp)", "Helt tett", "Tørker fort"], "correct": "Puster (slipper damp)"},
        {"q": "Ventilasjon ved lakkering?", "a": ["Hindre løsemidler", "Tørke fort", "Ingenting"], "correct": "Hindre løsemidler"},
        {"q": "Hva brukes sparkel til?", "a": ["Fylle ujevnheter", "Røre maling", "Skrape is"], "correct": "Fylle ujevnheter"},
        {"q": "Hva er glansgrad?", "a": ["Refleksjon av lys", "Pris", "Tykkelse"], "correct": "Refleksjon av lys"},
        {"q": "Verktøy for store flater?", "a": ["Rulle", "Pensel", "Svampe"], "correct": "Rulle"},
        {"q": "Sjekk i SDB for lakk?", "a": ["Verneutstyr/herdetid", "Farge", "Pris"], "correct": "Verneutstyr/herdetid"},
        {"q": "Hva er fiberreising?", "a": ["Treverk reiser seg ved fukt", "Feil pensel", "Flassing"], "correct": "Treverk reiser seg ved fukt"},
        {"q": "Male i sterkt sollys?", "a": ["Kan flasse/tørke fort", "Solbrent", "Feil farge"], "correct": "Kan flasse/tørke fort"},
        {"q": "Hva er NCS?", "a": ["Fargesystem", "Hemmelig kode", "Dato"], "correct": "Fargesystem"},
        {"q": "Filler med linolje?", "a": ["Tett metallboks", "Restavfall", "Henge opp"], "correct": "Tett metallboks"},
        {"q": "Hva gjør maskeringstape?", "a": ["Beskytter områder", "Fester tapet", "Reparerer"], "correct": "Beskytter områder"},
        {"q": "Fordel med vannbasert maling?", "a": ["Miljø og helse", "Lukt", "Pris"], "correct": "Miljø og helse"}
    ]
}

# --- 3. LOGIKK FOR MENY OG NAVIGASJON ---
st.sidebar.title("🏗️ Byggeplassen")
st_lottie(lottie_builder, height=120)

side = st.sidebar.radio("Hovedmeny", ["📍 Oversikt", "❓ Kunnskapstest", "📝 Loggbok (Utplassering)"])

if side == "📍 Oversikt":
    st.markdown("<h1 class='main-title'>Velkommen til Byggfag-Portalen</h1>", unsafe_allow_html=True)
    st.write("Velg ditt programområde under for informasjon:")
    valgt = st.selectbox("Programområde:", list(quiz_data.keys()))
    
    st.markdown(f"""
    <div class='category-card'>
        <h3>Info om {valgt}</h3>
        <p>Her lærer du om verktøy, materialer og sikkerhet innen {valgt.lower()}faget.</p>
        <p><i>Tips: Gå til 'Kunnskapstest' i menyen for å teste deg selv!</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    

elif side == "❓ Kunnskapstest":
    st.markdown("<h1 class='main-title'>Kunnskapstest</h1>", unsafe_allow_html=True)
    fag = st.selectbox("Hvilket fag vil du testes i?", list(quiz_data.keys()))
    
    if 'q_idx' not in st.session_state or 'current_fag' not in st.session_state or st.session_state.current_fag != fag:
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.current_fag = fag

    if st.session_state.q_idx < 15:
        q_list = quiz_data[fag]
        current_q = q_list[st.session_state.q_idx]
        
        # Progresjonslinje
        prosent = (st.session_state.q_idx / 15)
        st.progress(prosent, text=f"Byggeprosess: {int(prosent*100)}%")
        
        st.markdown(f"""
        <div class='category-card'>
            <h4>Spørsmål {st.session_state.q_idx + 1}</h4>
            <p style='font-size: 18px;'>{current_q['q']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        valg = st.radio("Velg ditt svar:", current_q['a'], key=f"radio_{st.session_state.q_idx}")
        
        if st.button("Bekreft svar"):
            if valg == current_q['correct']:
                st.success("Riktig utført! 🔨")
                st.session_state.score += 1
            else:
                st.error(f"Feil! Riktig svar var: {current_q['correct']}")
            
            st.session_state.q_idx += 1
            st.rerun()
    else:
        st.balloons()
        st.markdown(f"### 🏆 Test ferdig! Din score: {st.session_state.score} / 15")
        if st.button("Ta testen på nytt"):
            st.session_state.q_idx = 0
            st.session_state.score = 0
            st.rerun()

elif side == "📝 Loggbok (Utplassering)":
    st.markdown("<h1 class='main-title'>Digital Loggbok</h1>", unsafe_allow_html=True)
    st.info("Dokumenter arbeidet ditt mens du er ute i bedrift.")
    
    fag_logg = st.selectbox("Fagområde:", list(quiz_data.keys()))
    beskrivelse = st.text_area("Hva har du gjort i dag? (Bruk fagterminologi)")
    
    col1, col2 = st.columns(2)
    with col1:
        hms = st.checkbox("SJA utført")
        utstyr = st.checkbox("Bruker verneutstyr")
    with col2:
        orden = st.checkbox("Orden på arbeidsplassen")
        miljo = st.checkbox("Kildesortert avfall")

    foto = st.camera_input("Dokumentasjon (Bilde av arbeid)")
    
    if st.button("Lagre dagens logg"):
        if foto and hms:
            st.success("Loggen er lagret og sendt til vurdering!")
        else:
            st.warning("Husk bilde og HMS-sjekk for å godkjenne dagen.")

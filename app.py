import streamlit as st

# --- 1. KONFIGURASJON OG AVANSERT MØRKT DESIGN ---
st.set_page_config(page_title="Byggfag Pro", page_icon="🏗️", layout="wide")

# CSS for å gjenskape Finora-menyen med HVIT tekst
st.markdown("""
    <style>
    /* Hovedbakgrunn */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    /* Tilpasset Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 40, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Styling av menyelementer - Her settes teksten til HVIT */
    .stRadio > div {
        background-color: transparent !important;
    }
    
    .stRadio label {
        background-color: transparent;
        color: #ffffff !important; /* HVIT TEKST */
        padding: 10px 15px !important;
        border-radius: 10px !important;
        margin-bottom: 5px !important;
        transition: 0.3s;
        display: flex;
        align-items: center;
        font-weight: 500;
        font-size: 16px;
    }

    /* Hover-effekt (når musen er over et valg) */
    .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }

    /* Valgt menyvalg (Lilla gradient som i malen) */
    .stRadio label[data-selected="true"] {
        background: linear-gradient(90deg, #8a2be2 0%, #da70d6 100%) !important;
        color: #ffffff !important; /* Forblir hvit på lilla bakgrunn */
        box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
    }

    /* Glassmorphism Kort for innhold */
    .category-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Titler og tekst i hovedvindu */
    .main-title {
        color: #ffffff;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    h1, h2, h3, h4, p, li {
        color: #ffffff !important;
    }

    /* Skjul standard Streamlit header */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. KOMPLETT SPØRSMÅLSBANK (Alle 6 programmer à 15 spørsmål) ---
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
    "Anleggsteknikk": [
        {"q": "Hva må sjekkes før graving nær kabler?", "a": ["Ledningskart", "Værmelding", "Jordfarge"], "correct": "Ledningskart"},
        {"q": "Hva gjøres før man forlater en maskin?", "a": ["Senke utstyr til bakken", "La motoren gå", "Løfte skuffa"], "correct": "Senke utstyr til bakken"},
        {"q": "Risiko i usikret grøft over 2 meter?", "a": ["Raseulykker", "Ingen risiko", "Støv"], "correct": "Raseulykker"},
        {"q": "Signal for 'Stopp'?", "a": ["Begge armer ut", "Vinke", "En hånd i lomma"], "correct": "Begge armer ut"},
        {"q": "Hvorfor daglig kontroll av maskin?", "a": ["Forebygge ulykker", "Pynt", "Tidsfordriv"], "correct": "Forebygge ulykker"},
        {"q": "Hva er komprimering?", "a": ["Pakke masser med vals", "Vanne jord", "Flytte stein"], "correct": "Pakke masser med vals"},
        {"q": "Hva brukes fiberduk til?", "a": ["Separasjon av masselag", "Varme", "Pynt"], "correct": "Separasjon av masselag"},
        {"q": "Hva er stikking?", "a": ["Markere høyder/linjer", "Fjerne gress", "Rydde skog"], "correct": "Markere høyder/linjer"},
        {"q": "Hvilken masse drenerer best?", "a": ["Pukk", "Leire", "Silt"], "correct": "Pukk"},
        {"q": "Hva brukes rotasjonslaser til?", "a": ["Kontrollere høyder", "Kappe rør", "Lys"], "correct": "Kontrollere høyder"},
        {"q": "Hva betyr WLL på en stropp?", "a": ["Maks lasteevne", "Lengde", "Produsent"], "correct": "Maks lasteevne"},
        {"q": "Søl av hydraulikkolje i natur?", "a": ["Absorbere/rapportere", "Dekk med grus", "Helle vann"], "correct": "Absorbere/rapportere"},
        {"q": "Hva betyr det å anhuke?", "a": ["Feste last til kran", "Grave", "Parkere"], "correct": "Feste last til kran"},
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
        {"q": "Fordel med rør-i-rør?", "a": ["Utskiftbart/sikkert", "Billigere plast", "Tøffere"], "correct": "Utskiftbart/sikkert"},
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
        {"q": "Hva er et forband?", "a": ["Mønster for styrke", "Bandasje", "Sement"], "correct": "Mønster for styrke"},
        {"q": "Maks fallhøyde for betong?", "a": ["1,5 meter", "5 meter", "10 meter"], "correct": "1,5 meter"},
        {"q": "Verneutstyr ved sement?", "a": ["Støvmaske/hansker", "Hørselvern", "Ingenting"], "correct": "Støvmaske/hansker"},
        {"q": "Hva er forskaling?", "a": ["Form for betong", "Hvilepause", "Verktøy"], "correct": "Form for betong"},
        {"q": "Hva er herdetid?", "a": ["Tid til full styrke", "Blanding", "Lunsj"], "correct": "Tid til full styrke"},
        {"q": "Stein i fundament?", "a": ["Leca/Betongblokk", "Tegl", "Skifer"], "correct": "Leca/Betongblokk"},
        {"q": "For mye vann i betongen?", "a": ["Svakere styrke", "Sterkere", "Ingenting"], "correct": "Svakere styrke"},
        {"q": "Hva er eksponeringsklasse?", "a": ["Miljøkrav (salt)", "Seere", "Pris"], "correct": "Miljøkrav (salt)"},
        {"q": "Hva måles med slumptest?", "a": ["Konsistens", "Mengde", "Temp"], "correct": "Konsistens"}
    ],
    "Overflateteknikk": [
        {"q": "Grunnarbeid før maling?", "a": ["Vask og mattsliping", "Male direkte", "Vann"], "correct": "Vask og mattsliping"},
        {"q": "Tapet på ujevn vegg?", "a": ["Ujevnheter synes", "Retter vegg", "Ingen effekt"], "correct": "Ujevnheter synes"},
        {"q": "Funksjon til grunning?", "a": ["Heft og metting", "Farge", "Billigere"], "correct": "Heft og metting"},
        {"q": "Hva er diffusjonsåpen?", "a": ["Puster (damp)", "Helt tett", "Tørker fort"], "correct": "Puster (damp)"},
        {"q": "Ventilasjon ved lakkering?", "a": ["Hindre løsemidler", "Tørke fort", "Ingenting"], "correct": "Hindre løsemidler"},
        {"q": "Hva brukes sparkel til?", "a": ["Fylle ujevnheter", "Røre maling", "Is"], "correct": "Fylle ujevnheter"},
        {"q": "Hva er glansgrad?", "a": ["Refleksjon av lys", "Pris", "Tykkelse"], "correct": "Refleksjon av lys"},
        {"q": "Verktøy for store flater?", "a": ["Rulle", "Pensel", "Svampe"], "correct": "Rulle"},
        {"q": "Sjekk i SDB for lakk?", "a": ["Verneutstyr/herdetid", "Farge", "Pris"], "correct": "Verneutstyr/herdetid"},
        {"q": "Hva er fiberreising?", "a": ["Treverk reiser seg", "Feil pensel", "Flassing"], "correct": "Treverk reiser seg"},
        {"q": "Male i sterkt sollys?", "a": ["Kan flasse", "Solbrent", "Feil farge"], "correct": "Kan flasse"},
        {"q": "Hva er NCS?", "a": ["Fargesystem", "Hemmelig kode", "Dato"], "correct": "Fargesystem"},
        {"q": "Filler med linolje?", "a": ["Tett metallboks", "Restavfall", "Henge"], "correct": "Tett metallboks"},
        {"q": "Hva gjør maskeringstape?", "a": ["Beskytter områder", "Fester tapet", "Reparerer"], "correct": "Beskytter områder"},
        {"q": "Fordel med vannbasert maling?", "a": ["Miljø og helse", "Lukt", "Pris"], "correct": "Miljø og helse"}
    ],
    "Klima & Miljø": [
        {"q": "Hva er ENØK?", "a": ["Redusere energibruk", "Slå av lys", "Ved"], "correct": "Redusere energibruk"},
        {"q": "Funksjon til ventilasjon?", "a": ["Luftkvalitet/fukt", "Kun kjøling", "Støy"], "correct": "Luftkvalitet/fukt"},
        {"q": "Hva er en varmepumpe?", "a": ["Flytter varme", "Ovn", "Beholder"], "correct": "Flytter varme"},
        {"q": "Hva er varmegjenvinning?", "a": ["Bruke varme fra luft", "Fyre to ganger", "Spare"], "correct": "Bruke varme fra luft"},
        {"q": "Hva er et passivhus?", "a": ["Lavt energibehov", "Ingen bor der", "Uten vindu"], "correct": "Lavt energibehov"},
        {"q": "Hvorfor tette lekkasjer?", "a": ["Varmetap/fuktskader", "Edderkopper", "Stillhet"], "correct": "Varmetap/fuktskader"},
        {"q": "Hva er U-verdi?", "a": ["Varmeisolasjon", "Strømbruk", "Vekt"], "correct": "Varmeisolasjon"},
        {"q": "Fornybar energikilde?", "a": ["Solenergi", "Olje", "Kull"], "correct": "Solenergi"},
        {"q": "Smart-hus system?", "a": ["Styrer lys/varme", "Smart hus", "Roboter"], "correct": "Styrer lys/varme"},
        {"q": "Hva er termografering?", "a": ["Finne kuldebruer", "Måle fukt", "Veiing"], "correct": "Finne kuldebruer"},
        {"q": "Sortering av avfall?", "a": ["Sparer energi", "Ryddig", "Lovpålagt"], "correct": "Sparer energi"},
        {"q": "Hva er en kuldebru?", "a": ["Leder varme ut raskt", "Isbro", "Isolasjon"], "correct": "Leder varme ut raskt"},
        {"q": "Faggruppe for inneklima?", "a": ["Ventilasjonsmontør", "Murer", "Tømrer"], "correct": "Ventilasjonsmontør"},
        {"q": "Fordel med vannbåren varme?", "a": ["Jevn varme", "Billig", "Tar ingen plass"], "correct": "Jevn varme"},
        {"q": "Hva er energimerking?", "a": ["Energitilstand", "Beboere", "Alder"], "correct": "Energitilstand"}
    ]
}

# --- 3. LOGIKK FOR MENY OG NAVIGASJON ---
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:20px;'>Finora Bygg</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:white; font-size:12px; margin-bottom:5px; font-weight:bold;'>MAIN</p>", unsafe_allow_html=True)
    side = st.radio("", ["🏠 Dashboard", "🤖 AI Veileder"], label_visibility="collapsed")
    
    st.markdown("<br><p style='color:white; font-size:12px; margin-bottom:5px; font-weight:bold;'>UTDANNINGSPROGRAM</p>", unsafe_allow_html=True)
    fag_valg = st.radio("", list(quiz_data.keys()), label_visibility="collapsed")
    
    st.markdown("<br><p style='color:white; font-size:12px; margin-bottom:5px; font-weight:bold;'>VERKTØY</p>", unsafe_allow_html=True)
    verktoy = st.radio("", ["🎯 Kunnskapstest", "📝 Loggbok"], label_visibility="collapsed")

# --- 4. HOVEDINNHOLD ---
if verktoy == "🎯 Kunnskapstest":
    st.markdown(f"<h1 class='main-title'>Sertifisering: {fag_valg}</h1>", unsafe_allow_html=True)
    
    # State handling
    if 'q_idx' not in st.session_state or 'current_fag' not in st.session_state or st.session_state.current_fag != fag_valg:
        st.session_state.q_idx = 0
        st.session_state.score = 0
        st.session_state.current_fag = fag_valg

    if st.session_state.q_idx < 15:
        curr = quiz_data[fag_valg][st.session_state.q_idx]
        st.progress(st.session_state.q_idx / 15)
        
        st.markdown(f"<div class='category-card'><h4>Spørsmål {st.session_state.q_idx + 1}</h4><p>{curr['q']}</p></div>", unsafe_allow_html=True)
        valg = st.radio("Ditt svar:", curr['a'], key=f"q_{st.session_state.q_idx}")
        
        if st.button("BEKREFT SVAR"):
            if valg == curr['correct']:
                st.success("Korrekt utført!")
                st.session_state.score += 1
            else:
                st.error(f"Feil. Riktig svar: {curr['correct']}")
            st.session_state.q_idx += 1
            st.rerun()
    else:
        st.balloons()
        st.markdown(f"<div class='category-card' style='text-align:center;'><h2>RESULTAT</h2><h1>{st.session_state.score} / 15</h1></div>", unsafe_allow_html=True)
        if st.button("TA TESTEN PÅ NYTT"):
            st.session_state.q_idx = 0
            st.rerun()

elif verktoy == "📝 Loggbok":
    st.markdown("<h1 class='main-title'>Digital Loggbok</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='category-card'>Dokumentasjon for utplassering i {fag_valg}</div>", unsafe_allow_html=True)
    st.text_area("Beskrivelse av dagens arbeid (HMS og utførelse):")
    st.camera_input("Dokumentasjon (Bilde av arbeid)")
    st.button("SEND TIL LÆRER")

else: # Dashboard
    st.markdown(f"<h1 class='main-title'>Dashboard - {fag_valg}</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='category-card'><h4>Din Fremdrift</h4><h2 style='color:#da70d6;'>8/15 mål</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='category-card'><h4>Status</h4><h2 style='color:#00ff00;'>Aktiv Lærling</h2></div>", unsafe_allow_html=True)

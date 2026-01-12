import streamlit as st

# Initialiser poengsum og nivå i "session_state" så de ikke nullstilles
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'level' not in st.session_state:
    st.session_state.level = "Lærling"

# --- DESIGN OG STIL ---
st.set_page_config(page_title="Byggfag Master", page_icon="🏗️")
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; border-top: 15px solid #FFD700; }
    .score-box { background-color: #343a40; color: #FFD700; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- TOPPANEL (Poeng og Nivå) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='score-box'><h3>POENG: {st.session_state.points}</h3></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='score-box'><h3>NIVÅ: {st.session_state.level}</h3></div>", unsafe_allow_html=True)
with col3:
    if st.session_state.points >= 50:
        st.session_state.level = "Fagarbeider"
        st.balloons()
    st.progress(min(st.session_state.points / 100, 1.0))

# --- HOVEDMENY ---
st.title("👷 Velkommen til Byggeplassen")
tema = st.sidebar.selectbox("Hva vil du utforske?", ["Hjem", "Quiz: Verktøy", "Leksjon: Betong", "Leksjon: Treverk"])

if tema == "Hjem":
    st.subheader("Klar for å klatre i gradene?")
    st.write("Samle poeng ved å svare på quizer og gå gjennom leksjoner. Du trenger **50 poeng** for å bli en byggmester!")
    st.image("forsidebilde.jpg", caption="Byggfag i fokus") # Pass på at navnet stemmer med filen du laster opp

elif tema == "Quiz: Verktøy":
    st.subheader("🔨 Verktøy-Quiz")
    st.write("Hva brukes dette verktøyet til?")
    st.image("vater.jpg", width=300) # Pass på at navnet stemmer
    
    svar = st.radio("Velg svar:", ["Slå inn spiker", "Sjekke om noe er rett", "Kutte treverket"])
    
    if st.button("Sjekk svar"):
        if svar == "Sjekke om noe er rett":
            st.success("Riktig! +10 poeng")
            st.session_state.points += 10
        else:
            st.error("Feil! Prøv igjen.")

elif tema == "Leksjon: Betong":
    st.subheader("🏗️ Leksjon: Betong")
    st.write("Betong er et av de viktigste materialene vi har...")
    # Legg inn din tekst fra notebook her


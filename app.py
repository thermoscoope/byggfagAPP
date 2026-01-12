import streamlit as st

# Konfigurasjon
st.set_page_config(page_title="Byggfag-Portalen", page_icon="🏗️")

# --- SIDEBAR (HOVEDMENY) ---
st.sidebar.title("🏗️ Byggfag-Navigasjon")
valgt_program = st.sidebar.selectbox(
    "Velg utdanningsprogram:",
    ["Hjem", "Tømrer", "Rørlegger", "Betong og mur", "Anleggsteknikk"]
)

valgt_modus = st.sidebar.radio(
    "Hva vil du gjøre?",
    ["ℹ️ Informasjon", "❓ Quiz & Spørsmål", "📝 Utplassering / Loggbok"]
)

# --- HOVEDINNHOLD ---

if valgt_program == "Hjem":
    st.title("Velkommen til Byggfag-appen! 👷‍♂️")
    st.write("Velg ditt utdanningsprogram i menyen til venstre for å starte.")
    st.image("https://images.unsplash.com/photo-1541888946425-d81bb19480c5?auto=format&fit=crop&q=80&w=500", caption="Fremtidens fagarbeidere")

else:
    st.title(f"{valgt_modus} for {valgt_program}")

    # --- MODUS: INFORMASJON ---
    if valgt_modus == "ℹ️ Informasjon":
        if valgt_program == "Tømrer":
            st.write("### Om Tømrerfaget")
            st.write("Som tømrer bygger du hus, hytter og andre trekonstruksjoner. Du lærer om alt fra grunnmur til ferdig tak.")
            st.info("Visste du at tømrere står for en stor del av verdiskapningen i norsk byggenæring?")
        else:
            st.write(f"Her kommer informasjon om {valgt_program}...")

    # --- MODUS: QUIZ & SPØRSMÅL ---
    elif valgt_modus == "❓ Quiz & Spørsmål":
        st.write("### Test din kunnskap!")
        
        if valgt_program == "Tømrer":
            svar = st.radio("Hva er standard avstand mellom stenderne i en vegg (c/c)?", 
                           ["30 cm", "60 cm", "90 cm"])
            if st.button("Sjekk svar"):
                if svar == "60 cm":
                    st.success("Riktig! Du er klar for byggeplassen.")
                else:
                    st.error("Feil, prøv igjen! Tips: Tenk på platebredder.")

    # --- MODUS: UTPLASSERING (DIN LOGGBOK) ---
    elif valgt_modus == "📝 Utplassering / Loggbok":
        st.write("### Dokumentasjon i bedrift")
        st.info(f"Du er nå utplassert som {valgt_program}. Fyll ut dagens logg:")
        
        beskrivelse = st.text_area("Hva har du lært i bedriften i dag?")
        hms_ok = st.checkbox("Jeg har fulgt bedriftens HMS-regler")
        bilde = st.camera_input("Ta bilde av dagens arbeid")

        if st.button("Lagre dagens logg"):
            if bilde and hms_ok:
                st.balloons()
                st.success("Loggen er lagret og klar for læreren din!")
            else:
                st.warning("Husk bilde og HMS-sjekk!")

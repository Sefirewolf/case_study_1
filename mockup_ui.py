import streamlit as st
import pandas as pd
import datetime

today = datetime.datetime.now()

nutzer = {
    "Name": ["Anton Angerer", "Bernhard Berger", "Christian Cerin", "Doris Dietmaier"],
    "Email": ["anton@example.com", "bernhard@example.com", "christian@example.com", "doris@example.com"],
    "Geburtsdatum": ["15.01.1995", "13.09.1999", "30.10.2000", "12.03.2003"]
}
nutzer_df = pd.DataFrame(nutzer)

reservations = {
    "Gerätename": ["Gerät A", "Gerät B", "Gerät B", "Gerät A"],
    "Datum": ["10.01.2025 - 15.01.2025", "11.01.2025 - 21.01.2025", "21.01.2025 - 25.01.2025", "30.01.2025 - 31.01.2025"]
}
reservations_df = pd.DataFrame(reservations)

maintenance = {
    "Gerät":["Gerät A", "Gerät B"],
    "Wartungstermin": ["03.03.2025" , "04.04.2025"],
    "Kosten": ["200.35€", "198.22€"]
    }
maintenance_df = pd.DataFrame(maintenance)

#sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungssystem" , "Wartungsmanagement"])

#page Logic
if page == "Geräte-Verwaltung":
    
    
    # Eine Überschrift der ersten Ebene
    st.title("Geräte-Verwaltung")
    # Eine Überschrift der zweiten Ebene
    st.write("# Geräteauswahl")
    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis
    current_device = st.selectbox(label=
    'Gerät auswählen'
    ,
    options = ["Gerät_A" , "Gerät_B"])
    st.write(F"Das ausgewählte Gerät ist {current_device}")

    #Fenster öffnen für Geräteverwaltung
    st.markdown("### Geräte verwalten")
    st.info("Wählen sie aus, was Sie tun möchten:")

    # Button für Bearbeiten/Löschen
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Gerät bearbeiten"):
            st.warning("Funktion ist im Mockup nicht möglich")

    with col2:
        if st.button("Gerät löschen"):
            st.warning("Funktion ist im Mockup nicht möglich")
    
    @st.dialog("Gerät hinzufügen")
    def add_device():
        st.text_input("Name")
        st.text_input("Herstellungsdatum")
        st.text_input("Verantwortlicher")

        if st.button("Submit"):
            st.rerun()
       
    if st.button("Gerät hinzufügen"):
        add_device()

elif page == "Nutzer-Verwaltung":
    # Eine Überschrift der ersten Ebene
    st.title("Nutzer-Verwaltung")
    # Eine Überschrift der zweiten Ebene
    st.write("# Nutzerauswahl")
    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis
    current_user = st.selectbox("Nutzer auswählen:", 
    nutzer_df["Name"])
    st.write(F"Das ausgewählte Gerät ist {current_user}")

    if current_user:
        user_info = nutzer_df[nutzer_df["Name"] == current_user].iloc[0]

        st.subheader(f"Details für {current_user}:")
        st.write(f"**Name:** {user_info['Name']}")
        st.write(f"**Email:** {user_info['Email']}")
        st.write(f"**Geburtsdatum:**    {user_info['Geburtsdatum']}")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Nutzer bearbeiten"):
            st.warning("Funktion ist im Mockup nicht möglich")

    with col2:
        if st.button("Nutzer löschen"):
            st.warning("Funktion ist im Mockup nicht möglich")
    
    @st.dialog("Nutzer hinzufügen")
    def add_user():
        st.text_input("Vorname Nachname")
        st.text_input("Emailadresse")
        st.text_input("Geburtsdatum (DD.MM.JJJJ)")

        if st.button("Submit"):
            st.rerun()
       
    if st.button("Nutzer hinzufügen"):
        add_user()
    
elif page == "Reservierungssystem":
    st.title("Reservierungssystem")

    @st.dialog("Reservierung hinzufügen")
    def add_reservation():
        st.date_input(
        	"Reservierungszeitraum wählen",
            (today, datetime.date(today.year, 12, 31)), 
        today,
        format="DD.MM.YYYY",
        )

        st.selectbox(label=
        'Gerät auswählen'
        ,
        options = ["Gerät_A" , "Gerät_B"] 
        )   
        st.text_input("Person")  

        if st.button("Submit"):
            st.rerun()

    st.subheader("Bestehende Reservierungen:")
    st.dataframe(reservations_df)
      
    if st.button("Reservierung hinzufügen"):
        add_reservation()
    

elif page == "Wartungsmanagement":
    st.title("Wartungsmanagement")
    st.dataframe(maintenance_df)

    @st.dialog("Nächsten Wartungstermin festlegen")
    def add_maintenance():
        st.date_input(
        	"Reservierungszeitraum wählen",
        today, 
        today,
        format="DD.MM.YYYY",
        )
        st.selectbox(label=
        'Gerät auswählen'
        ,
        options = ["Gerät_A" , "Gerät_B"])   
        
        st.number_input("Kosten")     

        if st.button("Submit"):
            st.rerun()

    if st.button("Wartung hinzufügen"):
        add_maintenance()
    
    st.write("### Kosten für dieses Quartal betragen 200,35€.")



    




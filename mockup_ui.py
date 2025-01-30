import streamlit as st # type: ignore
import pandas as pd
import datetime
from tinydb import TinyDB, Query
import classes as cl

#definieren der Datenbanken
user_db = TinyDB("user_db.json")
device_db = TinyDB("device_db.json")

#leeren der datenbanken
#user_db.truncate()
#device_db.truncate()

#Füllen der Datenbanken mit Beispielen, falls diese leer sind
if len(user_db) == 0:
    user_db.insert(cl.User("anton@example.com" , "Anton Angerer").add_to_db())
    user_db.insert(cl.User("bernhard@example.com" , "Bernhard Berger").add_to_db())

if len(device_db) == 0:

    user_query = Query()
    user_1 = user_db.get(user_query.user_id == "anton@example.com")
    user_2 = user_db.get(user_query.user_id == "bernhard@example.com")

    laptop_1 = cl.Device(1, "Laptop_1", user_1).add_to_db()
    laptop_2 = cl.Device(2, "Laptop_2", user_2).add_to_db()

    device_db.insert(laptop_1)
    device_db.insert(laptop_2)

today = datetime.datetime.now()

maintenance = {
    "Gerät":["Gerät A", "Gerät B"],
    "Wartungstermin": ["03.03.2025" , "04.04.2025"],
    "Kosten": ["200.35€", "198.22€"]
    }
maintenance_df = pd.DataFrame(maintenance)

user_query = Query()
users = user_db.all()
user_ids = [user["user_id"] for user in users]

device_query = Query()

#Liste von Device-IDs erstellen mithilfe der Datenbank
devices = device_db.all()
device_ids = [device["device_name"] for device in devices]


#sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Gehe zu", ["Geräte-Verwaltung", "Nutzer-Verwaltung", "Reservierungssystem" , "Wartungsmanagement"])

#page Logic
if page == "Geräte-Verwaltung":
   
    # Eine Überschrift der ersten Ebene
    st.title("Geräte-Verwaltung")
    # Eine Überschrift der zweiten Ebene
    st.write("# Geräteauswahl")
    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis
    current_device = st.selectbox( 'Gerät auswählen', device_ids)
    st.write(F"Das ausgewählte Gerät ist {current_device}")

    #Fenster öffnen für Geräteverwaltung
    st.markdown("### Geräte verwalten")
    st.info("Wählen sie aus, was Sie tun möchten:")

    # Button für Bearbeiten/Löschen
    col1, col2 = st.columns(2)

    #Logik hinter Bearbeitungsbutton
    with col1:
        if st.button("Gerät bearbeiten"):
            st.warning("Funktion ist im Mockup nicht möglich")

    #Logik hinter Löschenbutton
    with col2:
        if st.button("Gerät löschen"):
            device_db.remove(device_query.device_name == current_device)
            st.rerun()
    
    
    @st.dialog("Gerät hinzufügen")
    def add_device():
        device_id = st.text_input("Seriennummer")
        device_name = st.text_input("Name des Gerätes")
        resp_user = st.text_input("Verantwortlicher")
        
        temp_device = cl.Device(device_id , device_name , resp_user)

        if st.button("Submit"):
            device_db.insert(temp_device.add_to_db())
            st.rerun()


    if st.button("Gerät hinzufügen"):
        add_device()

elif page == "Nutzer-Verwaltung":

    # Eine Überschrift der ersten Ebene
    st.title("Nutzer-Verwaltung")
    # Eine Überschrift der zweiten Ebene
    st.write("# Nutzerauswahl")
    # Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis
    current_user = st.selectbox( 'Nutezr auswählen', user_ids)
    st.write(F"Der ausgewählte Nutezr ist {current_user}")

    if current_user:

        st.subheader(f"Details für {current_user}:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Nutzer bearbeiten"):
            st.warning("Funktion ist im Mockup nicht möglich")

    with col2:
        if st.button("Nutzer löschen"):
            user_db.remove(user_query.user_id == current_user)
            st.rerun()
    
    @st.dialog("Nutzer hinzufügen")
    def add_user():
        user_id = st.text_input("Email des Nutzers")
        user_name = st.text_input("Name des Nutzers")
        
        temp_user = cl.User(user_id , user_name)

        if st.button("Submit"):
            user_db.insert(temp_user.add_to_db())
            st.rerun()
       
    if st.button("Nutzer hinzufügen"):
        add_user()
    
elif page == "Reservierungssystem":

    st.title("Reservierungssystem")

    @st.dialog("Reservierung hinzufügen")
    def add_reservation():
        reservation_start = st.date_input(
        	"Reservierungsstart wählen", value = None, format="DD.MM.YYYY")

        reservation_end = st.date_input(
        	"Reservierungsende wählen", value = None, format="DD.MM.YYYY")
        
        res_device = st.selectbox(label=
        'Gerät auswählen'
        ,
        options = device_ids
        )   
        res_user = st.selectbox(label=
        'Nutzer auswählen'
        ,
        options = user_ids
        )       

        device = device_db.get(device_query.device_name == res_device)
        user = user_db.get(user_query.user_id == res_user)

        if st.button("Submit"):
            device.reserve_device(user, reservation_start, reservation_end)
            st.rerun()

    st.subheader("Bestehende Reservierungen:")
      
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



    




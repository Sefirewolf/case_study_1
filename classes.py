from datetime import datetime



#Definierung der Klassen
class User:

    #initialisieren der Klasse
    def __init__(self, user_id: str, user_name: str): 

        self.user_id = user_id
        self.user_name = user_name

    #wiedergabe der Attribute
    def __repr__(self):

        return f"User(id = {self.user_id}, name = '{self.user_name}')"   


class Device:

    #initialisieren der Klasse
    def __init__(self, device_id: int, device_name: str, resp_user: User):
        
        self.device_id = device_id
        self.device_name = device_name
        self.responsible_user = resp_user
        self.last_update = None
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __last_update(self):

        return f"Letzte Wartung: '{self.last_update}'"

    def __creation_date(self):

        return f"Erstellung: '{self.creation_date}'"

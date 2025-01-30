from tinydb import TinyDB, Query
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

    def add_to_db(self):
        
        return {
            "user_id": self.user_id,
            "user_name": self.user_name
        }

class Device:
    def __init__(self, device_id, name, assigned_user=None):
        self.device_id = device_id
        self.name = name
        self.assigned_user = assigned_user
        self.reservations = []  # List of reservation dictionaries
    
    def add_to_db(self):
        """Convert device data to a dictionary for database storage."""
        return {
            'device_id': self.device_id,
            'name': self.name,
            'assigned_user': self.assigned_user['user_id'] if self.assigned_user else None,
            'reservations': self.reservations
        }
    
    def reserve_device(self, user, start_time, end_time):
        """Reserve the device if it's available during the given timeframe."""
        if self.is_available(start_time, end_time):
            self.reservations.append({
                'user': user['user_id'],
                'start_time': start_time,
                'end_time': end_time
            })
            return f"Device {self.name} reserved for {user['user_id']} from {start_time} to {end_time}."
        return f"Device {self.name} is not available during this time."
    
    def is_available(self, start_time, end_time):
        """Check if the device is available during the given timeframe."""
        for res in self.reservations:
            if not (end_time <= res['start_time'] or start_time >= res['end_time']):
                return False
        return True
    
    def update_reservation(self, user, new_start_time, new_end_time):
        """Update an existing reservation."""
        for res in self.reservations:
            if res['user'] == user['user_id']:
                if self.is_available(new_start_time, new_end_time):
                    res['start_time'] = new_start_time
                    res['end_time'] = new_end_time
                    return f"Reservation updated for {self.name}: {new_start_time} - {new_end_time}."
                return "New timeframe conflicts with an existing reservation."
        return "No existing reservation found."
    
    def remove_reservation(self, user):
        """Remove a reservation for the given user."""
        self.reservations = [res for res in self.reservations if res['user'] != user['user_id']]
        return f"Reservation for {self.name} by {user['user_id']} removed."

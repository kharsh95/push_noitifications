import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def schedule_events():
    event_data = {
        "user_id": "12343",
        "events": [
            {
                "event_id": "event_1",
                "scheduled_time": "2024-09-10T15:00:00",
                "message": "Event 1 Notification"
            },
            {
                "event_id": "event_2",
                "scheduled_time": "2024-09-10T17:00:00",
                "message": "Event 2 Notification"
            },
            {
                "event_id": "event_3",
                "scheduled_time": "2024-09-10T18:00:00",
                "message": "Event 3 Notification"
            }
        ]
    }
    db.collection("scheduled_events").add(event_data)
    print("Events scheduled for user 12343")

schedule_events()
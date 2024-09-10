import firebase_admin
from firebase_admin import credentials, firestore, messaging
from datetime import datetime

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def send_push_notification(message):
        fcm_token = "f88Y6lKNQ8-lwkAFNWon1j:APA91bHlPt_89lBzJAflRNTIYsuhHKWmZUZ7Le8DnBvsEUKF5VDVQx3tP0MiUmWbBsLNNgjNSbSKB7cEH4fzqWMg3-7N__iRXgRl1MLdm7Gp_g3wPzmIQky5pyJ7mLp2rats3jKY3bR2"

        message = messaging.Message(
            notification=messaging.Notification(
                title='Scheduled Event',
                body=message,
            ),
            token=fcm_token,
        )

        res = messaging.send(message)
        print(f"Successfully sent notification: {res}")


# Function to check for events and send notifications
# def check_and_send_notifications():
#     # Get current time in ISO format
#     now = datetime.utcnow().isoformat() + 'Z'

#     # Query Firestore for events scheduled before or at current time
#     scheduled_events = db.collection("scheduled_events").where('events.schedulced_time', '<=', now).get()

#     for doc in scheduled_events:
#         event_data = doc.to_dict()
#         user_id = event_data["user_id"]

#         # Send notifications for each event
#         for event in event_data["events"]:
#             send_push_notification(event["message"])

#         # Optionally: Remove the event document after sending notification
#         db.collection("scheduled_events").document(doc.id).delete()

# # Call the function to check and send notifications
# check_and_send_notifications()
send_push_notification("E1")
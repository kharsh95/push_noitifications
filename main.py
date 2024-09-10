import firebase_admin
from firebase_admin import credentials, firestore, messaging
from datetime import datetime
from firebase_functions import scheduler_fn

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def send_push_notification(message, time):
    fcm_token = "f88Y6lKNQ8-lwkAFNWon1j:APA91bHlPt_89lBzJAflRNTIYsuhHKWmZUZ7Le8DnBvsEUKF5VDVQx3tP0MiUmWbBsLNNgjNSbSKB7cEH4fzqWMg3-7N__iRXgRl1MLdm7Gp_g3wPzmIQky5pyJ7mLp2rats3jKY3bR2"
    
    notification_message = messaging.Message(
        notification=messaging.Notification(
            title=str(time),
            body=message,
        ),
        token=fcm_token,
    )

    res = messaging.send(notification_message)
    print(f"Successfully sent notification: {res}")

def input_message():
    message = input("Enter the message to be sent: ")
    time = input("Enter time at which notification is to be sent (epoch time): ")

    try:
        epoch_time = int(time)
    except ValueError:
        print("Invalid epoch time entered.")
        return

    local_time = datetime.fromtimestamp(epoch_time)
    epoch_now = int(datetime.now().timestamp())
    print(f"Time difference (seconds): {epoch_time - epoch_now}")

    event_data = {
        "epoch_time": epoch_time,
        "time": local_time,
        "message": message,
        "notificationSent": False
    }

    db.collection("scheduled_events").add(event_data)
    print(f"Notification scheduled for: {local_time}")

@scheduler_fn.on_schedule(schedule="* * * * *") 
def check_and_send_notifications() -> None:
    print("Scheduler function triggered")

    current_time = int(datetime.now().timestamp())
    query = db.collection("scheduled_events")\
        .where("epoch_time", "<=", current_time)\
        .where("notificationSent", "==", False).stream()

    for doc in query:
        data = doc.to_dict()
        message = data.get("message")
        scheduled_time = datetime.fromtimestamp(data.get("epoch_time"))

        send_push_notification(message, scheduled_time)

        doc.reference.update({
            "notificationSent": True
        })

    print("Checked for notifications to send.")

input_message()

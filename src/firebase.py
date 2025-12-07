import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)


async def send_push_notification(token: str, title: str, body: str, type: str, data: dict | None = None):
    print(f"[Firebase] Sending push notification to token: {token}, title: {title}, body: {body}, data: {data}", flush=True)
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        android=messaging.AndroidConfig(
            priority='high',
            collapse_key=type,
            notification=messaging.AndroidNotification(
                sound='default',
                tag=type
            )
        ),
        apns=messaging.APNSConfig(
            headers={'apns-priority': '10'},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                    thread_id=type
                )
            )
        )
    )
    try:
        response = messaging.send(message)
        print(f"[Firebase] Push notification sent: {response}", flush=True)
    except Exception as e:
        print(f"[Firebase] Failed to send push: {e}", flush=True)
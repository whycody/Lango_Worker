import os
import firebase_admin
from firebase_admin import credentials, messaging, get_app, exceptions
from dotenv import load_dotenv

TOKEN_INVALID = "token_invalid"

load_dotenv()

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")

try:
    get_app()
except ValueError:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)


async def send_push_notification(token: str, title: str, body: str, type: str, data: dict | None = None):
    print(f"[Firebase] Sending push notification to token: {token}, title: {title}, body: {body}, data: {data}",
          flush=True)
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
            headers={
                'apns-priority': '10',
                'apns-collapse-id': type
            },
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
        return True
    except exceptions.NotFoundError as e:
        print(f"[Firebase] Failed to send push: {e}", flush=True)
        return TOKEN_INVALID
    except Exception as e:
        print(f"[Firebase] Failed to send push: {e}", flush=True)
        return False

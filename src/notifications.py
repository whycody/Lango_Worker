from datetime import datetime
from mongo import db
from fcm import messaging
import datetime


async def process_notifications():
    now = datetime.datetime.now(datetime.timezone.utc)

    users = db.users.find({
        "notifications.enabled": True,
        "notifications.deviceTokens.0": {"$exists": True}
    })

    for user in users:
        for device in user["notifications"]["deviceTokens"]:
            messaging.send(
                messaging.Message(
                    token=device["token"],
                    notification=messaging.Notification(
                        title="Lango",
                        body="Powiadomienie z workera"
                    )
                )
            )
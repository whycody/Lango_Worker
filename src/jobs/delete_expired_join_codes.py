from datetime import datetime, timezone
from pymongo.collection import Collection


def delete_expired_join_codes(db: Collection):
    print("Deleting expired bundle join codes...", flush=True)
    try:
        now = datetime.now(timezone.utc)
        result = db.bundle_join_codes.delete_many({"expireAt": {"$lt": now}})
        print(f"Deleted {result.deleted_count} expired bundle join codes.", flush=True)
    except Exception as e:
        print("Failed to delete expired bundle join codes:", e, flush=True)

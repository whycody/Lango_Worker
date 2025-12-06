import firebase_admin
from firebase_admin import credentials, messaging
import os

if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS")

    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.initialize_app()
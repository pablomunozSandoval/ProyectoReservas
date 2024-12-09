import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Firebase
cred_path = os.path.join(BASE_DIR, 'config', 'reservasbd-a0564-firebase-adminsdk-xmza5-8c108f13d9.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Inicializa el cliente de Firestore
db = firestore.client()
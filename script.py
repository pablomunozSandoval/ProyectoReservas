# add_doctors.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Configurar Firebase
BASE_DIR = Path(__file__).resolve().parent
cred_path = os.path.join(BASE_DIR, 'config', 'reservasbd-a0564-firebase-adminsdk-xmza5-8c108f13d9.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Inicializar Firestore
db = firestore.client()

# Datos de los doctores
DOCTORES = [
    {
        "id": 1,
        "name": "Dr. John Smith",
        "specialty": "Cardiología",
        "description": "Especialista en enfermedades del corazón con más de 15 años de experiencia.",
        "schedule": "Lunes a Viernes, 9:00 AM - 3:00 PM",
        "available": True,
    },
    {
        "id": 2,
        "name": "Dra. Emily Carter",
        "specialty": "Pediatría",
        "description": "Atención especializada para niños y adolescentes.",
        "schedule": "Lunes a Viernes, 10:00 AM - 5:00 PM",
        "available": True,
    },
    {
        "id": 3,
        "name": "Dr. Carlos Martínez",
        "specialty": "Neurología",
        "description": "Experto en trastornos del sistema nervioso.",
        "schedule": "Martes y Jueves, 8:00 AM - 1:00 PM",
        "available": False,
    },
    {
        "id": 4,
        "name": "Dra. Ana López",
        "specialty": "Dermatología",
        "description": "Especialista en problemas de la piel.",
        "schedule": "Miércoles y Viernes, 9:00 AM - 2:00 PM",
        "available": True,
    },
    {
        "id": 5,
        "name": "Dr. Michael Brown",
        "specialty": "Ortopedia",
        "description": "Tratamiento de lesiones musculoesqueléticas.",
        "schedule": "Lunes a Jueves, 11:00 AM - 4:00 PM",
        "available": True,
    },
]

# Ingresar datos en Firestore
for doctor in DOCTORES:
    doc_ref = db.collection('doctors').document(str(doctor['id']))
    doc_ref.set(doctor)

print("Datos de los doctores ingresados correctamente en Firestore.")
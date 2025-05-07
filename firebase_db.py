import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase-credentials.json")  # Baixe do console Firebase
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://pizzariadelicious-default-rtdb.firebaseio.com"
})

def salvar_dado(path, dados):
    ref = db.reference(path)
    ref.push(dados)

def buscar_dados(path):
    ref = db.reference(path)
    return ref.get()

import firebase_admin
from firebase_admin import credentials, db
import os
import json

# Carrega as credenciais do Firebase da variável de ambiente
firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
cred_dict = json.loads(firebase_json)

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    "databaseURL": os.environ.get("FIREBASE_DB_URL")
})

def salvar_dado(path, dados):
    ref = db.reference(path)
    ref.push(dados)

def buscar_dados(path):
    ref = db.reference(path)
    return ref.get()

import json
import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials


def inicializar_firebase(base_dir=None):
    """
    Inicializa Firebase Admin una sola vez.

    En Render utiliza la variable FIREBASE_CREDENTIALS.
    En local utiliza secrets/firebase-service-account.json.
    """

    if firebase_admin._apps:
        return

    credenciales_json = os.getenv("FIREBASE_CREDENTIALS")

    if credenciales_json:
        try:
            credenciales_dict = json.loads(credenciales_json)
            credencial = credentials.Certificate(credenciales_dict)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "La variable FIREBASE_CREDENTIALS no contiene un JSON válido."
            ) from error
    else:
        directorio_base = (
            Path(base_dir)
            if base_dir is not None
            else Path(__file__).resolve().parent
        )

        ruta_credenciales = (
            directorio_base
            / "secrets"
            / "firebase-service-account.json"
        )

        if not ruta_credenciales.exists():
            print(
                "ADVERTENCIA: Firebase no fue inicializado porque no se "
                "encontraron credenciales."
            )
            return

        credencial = credentials.Certificate(
            str(ruta_credenciales)
        )

    firebase_admin.initialize_app(credencial)
    print("Firebase Admin inicializado correctamente.")
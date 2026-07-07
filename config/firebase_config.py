"""Inicialização única e centralizada do Firebase.

Todas as credenciais vivem aqui (via .env). Sem credenciais,
`get_firestore()` retorna None e a aplicação usa armazenamento local.
"""
from __future__ import annotations

from pathlib import Path

from config.settings import FIREBASE_CREDENTIALS_PATH

_app = None


def get_firestore():
    """Retorna o cliente Firestore ou None (modo local)."""
    global _app
    if not FIREBASE_CREDENTIALS_PATH or not Path(FIREBASE_CREDENTIALS_PATH).exists():
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if _app is None:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            _app = firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception:
        return None

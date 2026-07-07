"""Persistência de usuários: Firestore quando disponível, JSON local caso contrário.

Uma única interface (`UserStore`) para que o restante da aplicação
não saiba (nem precise saber) onde os dados vivem.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from config.firebase_config import get_firestore
from config.settings import LOCAL_DATA_DIR
from models.user import User


class UserStore:
    """Repositório de usuários (Firestore → coleção 'users'; local → .local_data/)."""

    def __init__(self) -> None:
        self._db = get_firestore()
        if self._db is None:
            LOCAL_DATA_DIR.mkdir(exist_ok=True)

    # ---------- API pública ----------
    @property
    def backend(self) -> str:
        return "firebase" if self._db else "local"

    def load(self, uid: str) -> Optional[User]:
        if self._db:
            doc = self._db.collection("users").document(uid).get()
            return User.from_dict(doc.to_dict()) if doc.exists else None
        path = self._path(uid)
        if path.exists():
            return User.from_dict(json.loads(path.read_text(encoding="utf-8")))
        return None

    def save(self, user: User) -> None:
        if self._db:
            self._db.collection("users").document(user.uid).set(user.to_dict())
            return
        self._path(user.uid).write_text(
            json.dumps(user.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def list_users(self) -> list[User]:
        """Todos os usuários (painel do professor)."""
        if self._db:
            return [User.from_dict(d.to_dict())
                    for d in self._db.collection("users").stream() if d.to_dict()]
        out = []
        for p in sorted(LOCAL_DATA_DIR.glob("user_*.json")):
            try:
                out.append(User.from_dict(json.loads(p.read_text(encoding="utf-8"))))
            except (json.JSONDecodeError, OSError):
                continue
        return out

    def delete(self, uid: str) -> None:
        """Apaga todos os dados do usuário (direito de exclusão — LGPD)."""
        if self._db:
            self._db.collection("users").document(uid).delete()
            return
        self._path(uid).unlink(missing_ok=True)

    # ---------- interno ----------
    @staticmethod
    def _path(uid: str) -> Path:
        return LOCAL_DATA_DIR / f"user_{uid}.json"

"""=====================================================================
SERVIÇO ADMIN — CRUD de questões/materiais + allowlist + imagens.
=====================================================================
Persiste via ContentRepository (Firestore quando há credenciais, disco
caso contrário). Após qualquer escrita, limpa os caches de leitura.
=====================================================================
"""
from __future__ import annotations

import re
from typing import Any

from config.settings import BASE_DIR
from services.content_repository import ContentRepository


class AdminService:
    def __init__(self) -> None:
        self._repo = ContentRepository()

    @property
    def backend(self) -> str:
        return self._repo.backend

    # ---------- questões ----------
    def save_question(self, data: dict[str, Any]) -> str:
        ref = self._repo.save_question(data)
        self._clear_caches()
        return ref

    def delete_question(self, qid: str) -> None:
        self._repo.delete_question(qid)
        self._clear_caches()

    # ---------- materiais ----------
    def save_material(self, data: dict[str, Any]) -> str:
        ref = self._repo.save_material(data)
        self._clear_caches()
        return ref

    def delete_material(self, mid: str) -> None:
        self._repo.delete_material(mid)
        self._clear_caches()

    # ---------- imagens ----------
    def save_image(self, file_bytes: bytes, filename: str) -> str:
        return self._repo.save_image(file_bytes, filename)

    # ---------- allowlist ----------
    @staticmethod
    def add_email(email: str) -> bool:
        """Insere um e-mail em ALLOWED_EMAILS no arquivo de config."""
        email = email.strip().lower()
        cfg = BASE_DIR / "config" / "access_control.py"
        src = cfg.read_text(encoding="utf-8")
        if f'"{email}"' in src:
            return False
        pattern = r"(ALLOWED_EMAILS: list\[str\] = \[\n)"
        cfg.write_text(re.sub(pattern, rf'\1    "{email}",\n', src, count=1),
                       encoding="utf-8")
        return True

    @staticmethod
    def _clear_caches() -> None:
        import services.material_service as ms
        import services.question_service as qs
        qs._load_all.clear()
        ms._load_all.clear()

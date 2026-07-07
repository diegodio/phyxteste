"""=====================================================================
REPOSITÓRIO DE CONTEÚDO — Firestore quando há credenciais, disco senão.
=====================================================================
Questões e materiais criados pelo admin são gravados:

  • COM credenciais Firebase → coleções `questions` e `materials`
    no Firestore (sobrevivem a redeploys e filesystem efêmero).
  • SEM credenciais           → arquivos JSON em questions/ e materials/
    (comportamento original).

A LEITURA sempre faz o merge: JSONs do disco (conteúdo "seed" versionado
no repositório) + documentos do Firestore (conteúdo criado em produção).
Se um id existir nos dois, o Firestore vence (permite editar seeds).

Imagens: com FIREBASE_STORAGE_BUCKET definido no .env, sobem para o
Firebase Storage (URL pública); senão vão para assets/uploads/.
=====================================================================
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from config.firebase_config import get_firestore
from config.settings import BASE_DIR, QUESTIONS_DIR
from services.material_service import MATERIALS_DIR

UPLOADS_DIR = BASE_DIR / "assets" / "uploads"


class ContentRepository:
    def __init__(self) -> None:
        self._db = get_firestore()

    @property
    def backend(self) -> str:
        return "firebase" if self._db else "local"

    # ------------------------- leitura (merge) -------------------------
    def load_questions(self) -> list[dict[str, Any]]:
        return self._merge(self._from_disk(QUESTIONS_DIR), "questions")

    def load_materials(self) -> list[dict[str, Any]]:
        return self._merge(self._from_disk(MATERIALS_DIR), "materials")

    # ------------------------- escrita -------------------------
    def save_question(self, data: dict[str, Any]) -> str:
        if self._db:
            self._db.collection("questions").document(data["id"]).set(data)
            return f"Firestore › questions/{data['id']}"
        folder = QUESTIONS_DIR / data["prova"] / str(data["ano"])
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{data['id']}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path.relative_to(BASE_DIR))

    def save_material(self, data: dict[str, Any]) -> str:
        if self._db:
            self._db.collection("materials").document(data["id"]).set(data)
            return f"Firestore › materials/{data['id']}"
        folder = MATERIALS_DIR / data["tema"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{data['id']}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path.relative_to(BASE_DIR))

    # ------------------------- exclusão -------------------------
    def delete_question(self, qid: str) -> None:
        if self._db:
            self._db.collection("questions").document(qid).delete()
        for p in QUESTIONS_DIR.rglob(f"{qid}.json"):
            p.unlink(missing_ok=True)

    def delete_material(self, mid: str) -> None:
        if self._db:
            self._db.collection("materials").document(mid).delete()
        for p in MATERIALS_DIR.rglob(f"{mid}.json"):
            p.unlink(missing_ok=True)

    # ------------------------- imagens -------------------------
    def save_image(self, file_bytes: bytes, filename: str) -> str:
        """Salva imagem e retorna a referência (URL ou caminho relativo)."""
        import os
        bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET", "")
        if self._db and bucket_name:
            try:
                from firebase_admin import storage
                blob = storage.bucket(bucket_name).blob(f"uploads/{filename}")
                blob.upload_from_string(file_bytes)
                blob.make_public()
                return blob.public_url
            except Exception:
                pass  # cai para o disco
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        path = UPLOADS_DIR / filename
        path.write_bytes(file_bytes)
        return str(path.relative_to(BASE_DIR))

    # ------------------------- interno -------------------------
    @staticmethod
    def _from_disk(root: Path) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        if root.exists():
            for p in sorted(root.rglob("*.json")):
                try:
                    out.append(json.loads(p.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    continue
        return out

    def _merge(self, disk: list[dict], collection: str) -> list[dict[str, Any]]:
        by_id = {d["id"]: d for d in disk if "id" in d}
        if self._db:
            try:
                for doc in self._db.collection(collection).stream():
                    d = doc.to_dict()
                    if d and "id" in d:
                        by_id[d["id"]] = d  # Firestore vence
            except Exception:
                pass
        return list(by_id.values())

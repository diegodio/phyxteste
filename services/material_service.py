"""Leitura dinâmica dos materiais de estudo.

Estrutura (igual à das questões — só criar pastas/arquivos, sem tocar código):

    materials/<Tema>/<arquivo>.json

Formato do JSON:
{
  "id": "mec-texto-001",
  "titulo": "...",
  "tipo": "texto" | "video",
  "tema": "Mecânica",
  "descricao": "resumo curto",
  "conteudo": "markdown completo (para tipo=texto)",
  "video_url": "https://youtube.com/... (para tipo=video)",
  "autor": "opcional",
  "nivel": "Básico|Intermediário|Avançado"
}
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

import streamlit as st

from config.settings import BASE_DIR

MATERIALS_DIR = BASE_DIR / "materials"


@dataclass
class Material:
    id: str
    titulo: str
    tipo: str            # "texto" | "video"
    tema: str
    descricao: str = ""
    conteudo: str = ""
    video_url: str = ""
    autor: str = ""
    nivel: str = "Básico"


@st.cache_data(show_spinner=False)
def _load_all() -> list[dict]:
    """Carrega materiais: disco + Firestore (merge) — ver ContentRepository."""
    from services.content_repository import ContentRepository
    return ContentRepository().load_materials()


class MaterialService:
    def all(self) -> list[Material]:
        return [Material(**{k: v for k, v in r.items() if k in Material.__dataclass_fields__})
                for r in _load_all()]

    def temas(self) -> list[str]:
        return sorted({m.tema for m in self.all()})

    def by(self, tema: Optional[str] = None, tipo: Optional[str] = None) -> list[Material]:
        ms = self.all()
        if tema: ms = [m for m in ms if m.tema == tema]
        if tipo: ms = [m for m in ms if m.tipo == tipo]
        return ms

"""Leitura dinâmica e cacheada do banco de questões.

Estrutura: questions/<PROVA>/<ANO>/<id>.json — novas provas/anos entram
sem qualquer mudança de código.
"""
from __future__ import annotations

import json
import random
from typing import Iterable, Optional

import streamlit as st

from config.settings import QUESTIONS_DIR, SIMULADO_SIZE
from models.question import Question


@st.cache_data(show_spinner=False)
def _load_all() -> list[dict]:
    """Carrega questões: disco + Firestore (merge) — ver ContentRepository."""
    from services.content_repository import ContentRepository
    return ContentRepository().load_questions()


class QuestionService:
    """Consultas, filtros e sorteios sobre o banco de questões."""

    def all(self) -> list[Question]:
        return [Question.from_dict(r) for r in _load_all()]

    # ---------- metadados p/ filtros ----------
    def provas(self) -> list[str]:
        return sorted({q.prova for q in self.all()})

    def anos(self, prova: Optional[str] = None) -> list[int]:
        qs = self.filter(prova=prova) if prova else self.all()
        return sorted({q.ano for q in qs}, reverse=True)

    def temas(self) -> list[str]:
        return sorted({q.tema for q in self.all()})

    def subtemas(self, tema: Optional[str] = None) -> list[str]:
        qs = self.filter(tema=tema) if tema else self.all()
        return sorted({q.subtema for q in qs if q.subtema})

    def dificuldades(self) -> list[str]:
        ordem = ["Fácil", "Média", "Difícil"]
        found = {q.dificuldade for q in self.all()}
        return [d for d in ordem if d in found] + sorted(found - set(ordem))

    # ---------- filtro ----------
    def filter(self, *, prova: Optional[str] = None, ano: Optional[int] = None,
               tema: Optional[str] = None, subtema: Optional[str] = None,
               dificuldade: Optional[str] = None,
               temas: Optional[Iterable[str]] = None) -> list[Question]:
        qs = self.all()
        if prova:       qs = [q for q in qs if q.prova == prova]
        if ano:         qs = [q for q in qs if q.ano == ano]
        if tema:        qs = [q for q in qs if q.tema == tema]
        if temas:       qs = [q for q in qs if q.tema in set(temas)]
        if subtema:     qs = [q for q in qs if q.subtema == subtema]
        if dificuldade: qs = [q for q in qs if q.dificuldade == dificuldade]
        return qs

    # ---------- busca textual ----------
    def search(self, termo: str) -> list["Question"]:
        """Busca por palavra no enunciado, tema, subtema, prova ou tags."""
        t = (termo or "").strip().lower()
        if not t:
            return self.all()
        out = []
        for q in self.all():
            campos = " ".join([q.enunciado, q.tema, q.subtema, q.prova,
                               " ".join(q.tags)]).lower()
            if t in campos:
                out.append(q)
        return out

    def get(self, question_id: str) -> Optional["Question"]:
        return next((q for q in self.all() if q.id == question_id), None)

    def get_many(self, ids: list[str]) -> list["Question"]:
        idset = set(ids)
        return [q for q in self.all() if q.id in idset]

    # ---------- simulado ----------
    def draw_exam(self, temas: Iterable[str], n: int = SIMULADO_SIZE) -> list[Question]:
        pool = self.filter(temas=temas)
        random.shuffle(pool)
        return pool[:n]

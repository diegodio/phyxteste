"""Modelos de domínio: Questão e Alternativa."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class Alternative:
    id: str
    texto: str
    correta: bool = False


@dataclass
class Question:
    id: str
    prova: str
    ano: int
    tema: str
    subtema: str
    dificuldade: str
    enunciado: str
    alternativas: list[Alternative]
    resolucao: str = ""
    explicacao: str = ""
    habilidades: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    fonte: str = ""
    imagem: Optional[str] = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Question":
        alts = [Alternative(**a) for a in raw.get("alternativas", [])]
        return cls(
            id=raw["id"], prova=raw["prova"], ano=int(raw["ano"]),
            tema=raw["tema"], subtema=raw.get("subtema", ""),
            dificuldade=raw.get("dificuldade", "Média"),
            enunciado=raw["enunciado"], alternativas=alts,
            resolucao=raw.get("resolucao", ""), explicacao=raw.get("explicacao", ""),
            habilidades=raw.get("habilidades", []), tags=raw.get("tags", []),
            fonte=raw.get("fonte", raw["prova"]), imagem=raw.get("imagem"),
        )

    @property
    def correct_id(self) -> str:
        return next(a.id for a in self.alternativas if a.correta)

    def shuffled(self, seed: Optional[int] = None) -> list[Alternative]:
        """Alternativas embaralhadas (determinístico se seed for dado)."""
        alts = list(self.alternativas)
        random.Random(seed).shuffle(alts)
        return alts

"""Modelos de usuário e resultado de simulado."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExamResult:
    id: str
    data: str
    temas: list[str]
    total: int
    acertos: int
    tempo_gasto: int            # segundos
    xp_ganho: int
    respostas: list[dict[str, Any]]  # [{question_id, tema, dificuldade, prova, escolhida, correta_id, acertou, tempo}]

    @property
    def pct(self) -> float:
        return 100 * self.acertos / self.total if self.total else 0.0


@dataclass
class User:
    uid: str
    nome: str
    email: str = ""
    foto: str = ""
    demo: bool = False
    criado_em: str = field(default_factory=_now)
    ultimo_acesso: str = field(default_factory=_now)
    xp_total: int = 0
    xp_por_tema: dict[str, int] = field(default_factory=dict)
    simulados: list[dict[str, Any]] = field(default_factory=list)
    questoes_respondidas: int = 0
    favoritas: list[str] = field(default_factory=list)
    tempo_estudado: int = 0     # segundos
    streak: int = 0
    ultimo_dia_estudo: str = ""
    # --- SRS (revisão espaçada): question_id -> estado do card ---
    revisoes: dict[str, dict[str, Any]] = field(default_factory=dict)
    # --- histórico de questões avulsas (feedback imediato) ---
    avulsas: list[dict[str, Any]] = field(default_factory=list)
    # --- metas diárias: {"data": "YYYY-MM-DD", "meta": 10, "feitas": N} ---
    meta_diaria: dict[str, Any] = field(default_factory=dict)
    # --- ids de conquistas já desbloqueadas ---
    conquistas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "User":
        known = {f: raw.get(f) for f in cls.__dataclass_fields__ if f in raw}
        return cls(**known)  # type: ignore[arg-type]

    def touch_streak(self) -> None:
        """Atualiza a sequência de dias de estudo."""
        today = datetime.now(timezone.utc).date()
        last: Optional[datetime.date] = None
        if self.ultimo_dia_estudo:
            last = datetime.fromisoformat(self.ultimo_dia_estudo).date()
        if last == today:
            pass
        elif last and (today - last).days == 1:
            self.streak += 1
        else:
            self.streak = 1
        self.ultimo_dia_estudo = datetime.now(timezone.utc).isoformat()

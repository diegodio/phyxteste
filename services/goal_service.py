"""=====================================================================
METAS DIÁRIAS
=====================================================================
Guarda em `user.meta_diaria`: {"data": "YYYY-MM-DD", "meta": N, "feitas": N}.
A meta reinicia sozinha a cada novo dia. Edite DEFAULT_META abaixo.
=====================================================================
"""
from __future__ import annotations

from datetime import datetime, timezone

from models.user import User

DEFAULT_META = 10  # questões por dia


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


class GoalService:
    @staticmethod
    def _ensure(user: User) -> None:
        md = user.meta_diaria
        if md.get("data") != _today():
            user.meta_diaria = {"data": _today(),
                                "meta": md.get("meta", DEFAULT_META),
                                "feitas": 0}

    @classmethod
    def register(cls, user: User, n: int = 1) -> None:
        """Contabiliza `n` questões respondidas hoje."""
        cls._ensure(user)
        user.meta_diaria["feitas"] += n

    @classmethod
    def set_target(cls, user: User, meta: int) -> None:
        cls._ensure(user)
        user.meta_diaria["meta"] = max(1, meta)

    @classmethod
    def status(cls, user: User) -> dict:
        cls._ensure(user)
        md = user.meta_diaria
        pct = min(1.0, md["feitas"] / md["meta"]) if md["meta"] else 0.0
        return {"meta": md["meta"], "feitas": md["feitas"],
                "progresso": pct, "cumprida": md["feitas"] >= md["meta"]}

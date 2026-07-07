"""=====================================================================
REVISÃO ESPAÇADA (SRS) — algoritmo SM-2 simplificado.
=====================================================================

Cada questão respondida vira um "card" com estado guardado em
`user.revisoes[question_id]`:

    {
      "intervalo": int,     # dias até a próxima revisão
      "facilidade": float,  # fator de facilidade (>= 1.3)
      "repeticoes": int,    # acertos consecutivos
      "proxima": "ISO date",# quando volta a aparecer
      "ultima": "ISO date"  # última revisão
    }

Regra prática:
- Errou  → card reinicia (volta a aparecer amanhã).
- Acertou→ intervalo cresce (1 → 3 → intervalo*facilidade).

`due(user)` devolve os ids que já venceram (revisar hoje).
=====================================================================
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from models.user import User

_MIN_EF = 1.3


def _today() -> date:
    return datetime.now(timezone.utc).date()


class SRSService:
    @staticmethod
    def _new_card() -> dict[str, Any]:
        return {"intervalo": 0, "facilidade": 2.5, "repeticoes": 0,
                "proxima": _today().isoformat(), "ultima": ""}

    @classmethod
    def review(cls, user: User, question_id: str, acertou: bool) -> dict[str, Any]:
        """Atualiza (ou cria) o card após uma resposta."""
        card = user.revisoes.get(question_id, cls._new_card())
        ef = card["facilidade"]

        if acertou:
            reps = card["repeticoes"] + 1
            if reps == 1:
                intervalo = 1
            elif reps == 2:
                intervalo = 3
            else:
                intervalo = round(card["intervalo"] * ef)
            ef = max(_MIN_EF, ef + 0.1)
            card.update(repeticoes=reps, intervalo=intervalo, facilidade=ef)
        else:
            # errou: penaliza facilidade e reinicia o ciclo (revisa amanhã)
            ef = max(_MIN_EF, ef - 0.2)
            card.update(repeticoes=0, intervalo=1, facilidade=ef)

        prox = _today() + timedelta(days=card["intervalo"])
        card["proxima"] = prox.isoformat()
        card["ultima"] = _today().isoformat()
        user.revisoes[question_id] = card
        return card

    @staticmethod
    def due(user: User) -> list[str]:
        """IDs de questões vencidas (data de revisão <= hoje)."""
        hoje = _today()
        return [qid for qid, c in user.revisoes.items()
                if date.fromisoformat(c["proxima"]) <= hoje]

    @staticmethod
    def counts(user: User) -> dict[str, int]:
        """Resumo para dashboards: vencidas, agendadas, total."""
        hoje = _today()
        due = sum(1 for c in user.revisoes.values()
                  if date.fromisoformat(c["proxima"]) <= hoje)
        return {"vencidas": due,
                "agendadas": len(user.revisoes) - due,
                "total": len(user.revisoes)}

"""=====================================================================
PRÁTICA AVULSA (feedback imediato)
=====================================================================
Um único ponto de entrada — `answer_single()` — que ao responder uma
questão fora do simulado dispara TODOS os efeitos colaterais de forma
consistente:

  • concede XP no tema                (XPService)
  • atualiza o card de revisão        (SRSService)
  • conta para a meta diária          (GoalService)
  • incrementa questões respondidas
  • verifica conquistas               (AchievementService)
  • persiste o usuário                (AuthService)

Retorna um dicionário com o resultado para a UI montar o feedback.
=====================================================================
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from config.settings import XP_PER_CORRECT
from models.question import Question
from models.user import User
from services.achievement_service import AchievementService
from services.goal_service import GoalService
from services.srs_service import SRSService
from services.xp_service import XPService


class PracticeService:
    def __init__(self, auth) -> None:
        self._auth = auth

    def answer_single(self, question: Question, alt_id: str) -> dict[str, Any]:
        user: User = self._auth.current_user()
        acertou = alt_id == question.correct_id
        xp = XP_PER_CORRECT if acertou else 0

        if acertou:
            XPService.grant(user, question.tema, xp)

        SRSService.review(user, question.id, acertou)
        GoalService.register(user, 1)
        user.questoes_respondidas += 1
        user.avulsas.append({
            "question_id": question.id, "tema": question.tema,
            "acertou": acertou, "data": datetime.now(timezone.utc).isoformat(),
        })
        user.touch_streak()
        novas = AchievementService.check_new(user)
        self._auth.persist(user)

        return {"acertou": acertou, "xp": xp,
                "correta_id": question.correct_id,
                "conquistas": novas}

"""Ciclo de vida do simulado: montar, responder, finalizar e registrar."""
from __future__ import annotations

import time
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Optional

import streamlit as st

from models.question import Question
from models.user import ExamResult, User
from services.auth_service import AuthService
from services.question_service import QuestionService
from services.xp_service import XPService
from services.srs_service import SRSService
from services.goal_service import GoalService
from services.achievement_service import AchievementService

_KEY = "pc_exam"


class SimuladoService:
    def __init__(self, questions: QuestionService, auth: AuthService) -> None:
        self._q = questions
        self._auth = auth

    # ---------- estado ----------
    def active(self) -> Optional[dict[str, Any]]:
        return st.session_state.get(_KEY)

    def start(self, temas: list[str], timer_seconds: int, n: int | None = None) -> bool:
        exam = self._q.draw_exam(temas, n) if n else self._q.draw_exam(temas)
        if len(exam) < 1:
            return False
        st.session_state[_KEY] = {
            "id": uuid.uuid4().hex[:10],
            "temas": temas,
            "timer": timer_seconds,
            "inicio": time.time(),
            "questoes": exam,
            "seeds": {q.id: uuid.uuid4().int % 10_000 for q in exam},
            "respostas": {},           # question_id -> alternativa escolhida
            "idx": 0,
        }
        return True

    def answer(self, question_id: str, alt_id: str) -> None:
        self.active()["respostas"][question_id] = alt_id

    def time_left(self) -> Optional[int]:
        ex = self.active()
        if not ex or not ex["timer"]:
            return None
        return max(0, int(ex["timer"] - (time.time() - ex["inicio"])))

    # ---------- finalização ----------
    def finish(self) -> ExamResult:
        ex = st.session_state.pop(_KEY)
        user: User = self._auth.current_user()
        elapsed = int(time.time() - ex["inicio"])
        respostas: list[dict[str, Any]] = []
        acertos, xp_total, streak = 0, 0, 0

        for q in ex["questoes"]:
            q: Question
            escolhida = ex["respostas"].get(q.id)
            ok = escolhida == q.correct_id
            streak = streak + 1 if ok else 0
            xp = XPService.xp_for_answer(ok, streak)
            if ok:
                acertos += 1
                XPService.grant(user, q.tema, xp)
                xp_total += xp
            SRSService.review(user, q.id, ok)  # alimenta a revisão espaçada
            respostas.append({
                "question_id": q.id, "tema": q.tema, "prova": q.prova,
                "dificuldade": q.dificuldade, "escolhida": escolhida,
                "correta_id": q.correct_id, "acertou": ok,
            })

        result = ExamResult(
            id=ex["id"], data=datetime.now(timezone.utc).isoformat(),
            temas=ex["temas"], total=len(ex["questoes"]), acertos=acertos,
            tempo_gasto=elapsed, xp_ganho=xp_total, respostas=respostas,
        )
        user.simulados.append(asdict(result))
        user.questoes_respondidas += result.total
        user.tempo_estudado += elapsed
        GoalService.register(user, result.total)      # conta para a meta diária
        user.touch_streak()
        novas = AchievementService.check_new(user)     # medalhas desbloqueadas
        st.session_state["pc_new_achievements"] = novas
        self._auth.persist(user)
        st.session_state["pc_last_result"] = result
        st.session_state["pc_last_questions"] = ex["questoes"]
        return result

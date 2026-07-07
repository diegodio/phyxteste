"""Injeção de dependências simples (singletons por sessão)."""
from __future__ import annotations

import streamlit as st

from services.achievement_service import AchievementService
from services.auth_service import AuthService
from services.favorite_service import FavoriteService
from services.goal_service import GoalService
from services.material_service import MaterialService
from services.practice_service import PracticeService
from services.question_service import QuestionService
from services.simulado_service import SimuladoService
from services.srs_service import SRSService
from services.stats_service import StatsService
from services.storage_service import UserStore
from services.xp_service import XPService


@st.cache_resource(show_spinner=False)
def _store() -> UserStore:
    return UserStore()


def ctx() -> dict:
    store = _store()
    auth = AuthService(store)
    questions = QuestionService()
    return {
        "store": store,
        "auth": auth,
        "questions": questions,
        "materials": MaterialService(),
        "simulado": SimuladoService(questions, auth),
        "practice": PracticeService(auth),
        "stats": StatsService(),
        "xp": XPService(),
        "srs": SRSService(),
        "goals": GoalService(),
        "favorites": FavoriteService(),
        "achievements": AchievementService(),
    }

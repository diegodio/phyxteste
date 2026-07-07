"""Avaliação e desbloqueio de conquistas."""
from __future__ import annotations

from data.achievements import ACHIEVEMENTS
from models.user import User


class AchievementService:
    @staticmethod
    def check_new(user: User, stats=None) -> list[dict]:
        """Retorna conquistas recém-desbloqueadas (e as registra no usuário)."""
        novas = []
        for a in ACHIEVEMENTS:
            if a["id"] not in user.conquistas and a["check"](user, stats):
                user.conquistas.append(a["id"])
                novas.append(a)
        return novas

    @staticmethod
    def all_with_state(user: User) -> list[dict]:
        """Todas as conquistas com flag `unlocked`."""
        return [{**a, "unlocked": a["id"] in user.conquistas} for a in ACHIEVEMENTS]

"""Favoritar questões (usa o campo `user.favoritas` já existente)."""
from __future__ import annotations

from models.user import User


class FavoriteService:
    @staticmethod
    def toggle(user: User, question_id: str) -> bool:
        """Alterna favorito; retorna o novo estado (True = favoritada)."""
        if question_id in user.favoritas:
            user.favoritas.remove(question_id)
            return False
        user.favoritas.append(question_id)
        return True

    @staticmethod
    def is_fav(user: User, question_id: str) -> bool:
        return question_id in user.favoritas

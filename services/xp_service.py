"""Gamificação: XP por tema, níveis por trilha de cientistas."""
from __future__ import annotations

from typing import Optional

from config.settings import XP_BONUS_STREAK, XP_PER_CORRECT
from data.physicists import TRACKS
from models.user import User


class XPService:
    # ---------- ganho ----------
    @staticmethod
    def xp_for_answer(correct: bool, streak_in_exam: int) -> int:
        if not correct:
            return 0
        return XP_PER_CORRECT + XP_BONUS_STREAK * max(0, streak_in_exam - 1)

    @staticmethod
    def grant(user: User, tema: str, amount: int) -> None:
        user.xp_por_tema[tema] = user.xp_por_tema.get(tema, 0) + amount
        user.xp_total += amount

    # ---------- níveis ----------
    @staticmethod
    def track(tema: str) -> list[dict]:
        return TRACKS.get(tema, TRACKS["_default"])

    @classmethod
    def level_info(cls, tema: str, xp: int) -> dict:
        """Nível atual, próximo cientista e progresso no tema."""
        track = cls.track(tema)
        current: Optional[dict] = None
        nxt: Optional[dict] = None
        for sci in track:
            if xp >= sci["xp"]:
                current = sci
            elif nxt is None:
                nxt = sci
        idx = track.index(current) + 1 if current else 0
        if nxt:
            base = current["xp"] if current else 0
            prog = (xp - base) / (nxt["xp"] - base)
        else:
            prog = 1.0
        return {"nivel": idx, "atual": current, "proximo": nxt,
                "progresso": min(max(prog, 0.0), 1.0), "total_niveis": len(track)}

    @classmethod
    def overall_level(cls, user: User) -> int:
        return sum(cls.level_info(t, xp)["nivel"] for t, xp in user.xp_por_tema.items())

    @classmethod
    def unlocked(cls, user: User) -> list[tuple[str, dict]]:
        out: list[tuple[str, dict]] = []
        for tema, xp in user.xp_por_tema.items():
            for sci in cls.track(tema):
                if xp >= sci["xp"]:
                    out.append((tema, sci))
        return out

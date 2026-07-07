"""Estatísticas derivadas do histórico do usuário."""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from models.user import User


class StatsService:
    @staticmethod
    def exams_df(user: User) -> pd.DataFrame:
        if not user.simulados:
            return pd.DataFrame()
        df = pd.DataFrame(user.simulados)
        df["data"] = pd.to_datetime(df["data"])
        df["pct"] = 100 * df["acertos"] / df["total"]
        return df.sort_values("data")

    @staticmethod
    def answers_df(user: User) -> pd.DataFrame:
        rows: list[dict[str, Any]] = []
        for sim in user.simulados:
            for r in sim["respostas"]:
                rows.append({**r, "data": sim["data"]})
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows)
        df["data"] = pd.to_datetime(df["data"])
        return df

    # ---------- agregações ----------
    @classmethod
    def by(cls, user: User, col: str) -> pd.DataFrame:
        df = cls.answers_df(user)
        if df.empty:
            return df
        g = df.groupby(col)["acertou"].agg(["sum", "count"]).reset_index()
        g.columns = [col, "acertos", "total"]
        g["pct"] = 100 * g["acertos"] / g["total"]
        return g.sort_values("pct", ascending=False)

    @classmethod
    def by_habilidade(cls, user: User, question_service) -> pd.DataFrame:
        """Desempenho por habilidade/competência ENEM (campo `habilidades`)."""
        df = cls.answers_df(user)
        if df.empty:
            return pd.DataFrame()
        hmap = {q.id: q.habilidades for q in question_service.all()}
        rows = []
        for _, r in df.iterrows():
            for h in hmap.get(r["question_id"], []):
                rows.append({"habilidade": h, "acertou": r["acertou"]})
        if not rows:
            return pd.DataFrame()
        g = pd.DataFrame(rows).groupby("habilidade")["acertou"].agg(["sum", "count"]).reset_index()
        g.columns = ["habilidade", "acertos", "total"]
        g["pct"] = 100 * g["acertos"] / g["total"]
        return g.sort_values("pct")

    @classmethod
    def strongest_weakest(cls, user: User) -> tuple[Optional[str], Optional[str]]:
        g = cls.by(user, "tema")
        if g.empty:
            return None, None
        return g.iloc[0]["tema"], g.iloc[-1]["tema"]

    @staticmethod
    def accuracy(user: User) -> float:
        total = sum(s["total"] for s in user.simulados)
        hits = sum(s["acertos"] for s in user.simulados)
        return 100 * hits / total if total else 0.0

    @staticmethod
    def avg_time_per_question(user: User) -> float:
        total_q = sum(s["total"] for s in user.simulados)
        return user.tempo_estudado / total_q if total_q else 0.0

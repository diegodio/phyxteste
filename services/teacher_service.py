"""=====================================================================
SERVIÇO DO PROFESSOR — agregações da turma inteira.
=====================================================================
Lê todos os usuários do UserStore e produz visões de turma:
erros por tema, alunos em risco, atividade recente, ranking de XP.
=====================================================================
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from models.user import User
from services.storage_service import UserStore


class TeacherService:
    def __init__(self, store: UserStore) -> None:
        self._store = store

    def students(self) -> list[User]:
        """Todos os usuários não-demo (a 'turma')."""
        return [u for u in self._store.list_users() if not u.demo]

    # ---------- visões ----------
    def overview_df(self) -> pd.DataFrame:
        rows: list[dict[str, Any]] = []
        for u in self.students():
            total = sum(s["total"] for s in u.simulados)
            hits = sum(s["acertos"] for s in u.simulados)
            rows.append({
                "Aluno": u.nome, "Email": u.email,
                "XP": u.xp_total, "Questões": u.questoes_respondidas,
                "Acerto %": round(100 * hits / total, 1) if total else 0.0,
                "Streak": u.streak, "Simulados": len(u.simulados),
                "Último acesso": u.ultimo_acesso[:10],
            })
        return pd.DataFrame(rows)

    def theme_errors_df(self) -> pd.DataFrame:
        """Taxa de erro da turma por tema (onde a classe mais sofre)."""
        rows = []
        for u in self.students():
            for s in u.simulados:
                for r in s["respostas"]:
                    rows.append({"tema": r["tema"], "acertou": r["acertou"]})
        if not rows:
            return pd.DataFrame()
        df = pd.DataFrame(rows)
        g = df.groupby("tema")["acertou"].agg(["mean", "count"]).reset_index()
        g.columns = ["tema", "acerto", "respostas"]
        g["erro_pct"] = 100 * (1 - g["acerto"])
        return g.sort_values("erro_pct", ascending=False)

    def at_risk(self) -> list[dict[str, Any]]:
        """Alunos que merecem atenção: sem streak, baixa taxa ou inativos."""
        out = []
        hoje = datetime.now(timezone.utc)
        for u in self.students():
            total = sum(s["total"] for s in u.simulados)
            hits = sum(s["acertos"] for s in u.simulados)
            taxa = 100 * hits / total if total else None
            dias_off = (hoje - datetime.fromisoformat(u.ultimo_acesso)).days
            motivos = []
            if dias_off >= 7: motivos.append(f"{dias_off} dias sem acessar")
            if u.streak == 0: motivos.append("streak zerado")
            if taxa is not None and taxa < 50: motivos.append(f"acerto {taxa:.0f}%")
            if motivos:
                out.append({"nome": u.nome, "email": u.email, "motivos": motivos})
        return out

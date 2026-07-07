"""Painel do professor: visão agregada da turma.

Acesso: permissão "professor" (ou "*") em config/access_control.py.
"""
from __future__ import annotations

import streamlit as st

from components import charts
from components.ui import metric_card
from services.access_service import AccessService
from services.teacher_service import TeacherService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "professor")

teacher = TeacherService(c["store"])
alunos = teacher.students()

st.markdown("## 🧑‍🏫 Painel do professor")
st.caption("Visão agregada da turma — desempenho, temas críticos e alunos em risco.")

if not alunos:
    st.info("Nenhum aluno cadastrado ainda (contas demo não entram na turma).")
    st.stop()

df = teacher.overview_df()
cols = st.columns(4)
with cols[0]: metric_card("Alunos", str(len(alunos)), "na turma", "👥")
with cols[1]: metric_card("Questões", str(int(df["Questões"].sum())), "respondidas no total", "🧮")
with cols[2]: metric_card("Acerto médio", f"{df['Acerto %'].mean():.0f}%", "da turma", "🎯")
with cols[3]: metric_card("XP somado", str(int(df["XP"].sum())), "", "✨")

st.markdown("### 🚨 Alunos que merecem atenção")
risco = teacher.at_risk()
if not risco:
    st.success("Ninguém em risco no momento. 🎉")
for r in risco:
    st.markdown(f"- **{r['nome']}** ({r['email']}) — {', '.join(r['motivos'])}")

st.markdown("### 📉 Onde a turma mais erra")
erros = teacher.theme_errors_df()
if erros.empty:
    st.caption("Sem respostas de simulado registradas ainda.")
else:
    st.plotly_chart(charts.bar(erros, "tema", "erro_pct",
                               "Taxa de erro por tema (%)", charts.QUARK),
                    use_container_width=True)

st.markdown("### 🏆 Ranking da turma (XP)")
st.dataframe(df.sort_values("XP", ascending=False),
             use_container_width=True, hide_index=True)

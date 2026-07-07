"""Renderização de questões (consulta e simulado)."""
from __future__ import annotations

import streamlit as st

from components.ui import badge, badges_row
from config.settings import theme_meta
from models.question import Question
from utils.latex import render_md
from config.settings import BASE_DIR

_DIFF_KIND = {"Fácil": "green", "Média": "amber", "Difícil": "rose"}


def question_header(q: Question) -> None:
    meta = theme_meta(q.tema)
    badges_row(
        badge(f"📄 {q.prova}", "slate"),
        badge(f"📅 {q.ano}", "slate"),
        badge(f"{meta['icon']} {q.tema}"),
        badge(f"↳ {q.subtema}", "slate") if q.subtema else "",
        badge(q.dificuldade, _DIFF_KIND.get(q.dificuldade, "")),
    )


def question_full(q: Question) -> None:
    """Questão resolvida (modo consulta)."""
    with st.container(border=True):
        question_header(q)
        render_md(f"**{q.enunciado}**")
        if q.imagem:
            img = q.imagem if str(q.imagem).startswith("http") else str(BASE_DIR / q.imagem)
            st.image(img)
        for alt in q.alternativas:
            mark = "✅" if alt.correta else "◻️"
            st.markdown(f"{mark} **{alt.id})** {alt.texto}")
        with st.expander("📝 Resolução completa"):
            render_md(q.resolucao or "_Sem resolução cadastrada._")
        with st.expander("💡 Explicação conceitual"):
            render_md(q.explicacao or "_Sem explicação cadastrada._")

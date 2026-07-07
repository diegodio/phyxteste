"""=====================================================================
RENDERIZAÇÃO DE FÓRMULAS (LaTeX / KaTeX)
=====================================================================
Streamlit já renderiza LaTeX em markdown quando as fórmulas vêm entre
cifrões: inline `$...$` e bloco `$$...$$`.

`render_md(texto)` exibe markdown científico com segurança, e
`has_math()` detecta se há fórmula (útil para escolher o renderizador).

Nos JSON de questões/materiais, escreva física normalmente:
    "A força é $F = k\\dfrac{q_1 q_2}{d^2}$."
=====================================================================
"""
from __future__ import annotations

import re

import streamlit as st

_MATH = re.compile(r"\$.+?\$")


def has_math(text: str) -> bool:
    return bool(_MATH.search(text or ""))


def render_md(text: str) -> None:
    """Renderiza markdown com suporte a LaTeX (padrão do Streamlit)."""
    st.markdown(text or "", unsafe_allow_html=False)

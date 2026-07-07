"""Consulta de questões resolvidas com filtros e busca textual."""
from __future__ import annotations

import streamlit as st

from components.question_card import question_full
from services.access_service import AccessService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "questoes")

q, fav = c["questions"], c["favorites"]

st.markdown("## 🔎 Banco de questões")
st.caption("Filtre, busque, favorite e estude com resolução completa.")

# busca textual
termo = st.text_input("🔍 Buscar por palavra no enunciado, tema ou tags", "")

f1, f2, f3 = st.columns(3)
with f1:
    prova = st.selectbox("Vestibular / prova", ["Todos"] + q.provas())
with f2:
    anos = q.anos(None if prova == "Todos" else prova)
    ano = st.selectbox("Ano", ["Todos"] + [str(a) for a in anos])
with f3:
    tema = st.selectbox("Tema", ["Todos"] + q.temas())

f4, f5 = st.columns(2)
with f4:
    subtema = st.selectbox("Subtema", ["Todos"] + q.subtemas(None if tema == "Todos" else tema))
with f5:
    dif = st.selectbox("Dificuldade", ["Todas"] + q.dificuldades())

results = q.search(termo) if termo else q.all()
def _keep(x):
    return ((prova == "Todos" or x.prova == prova)
            and (ano == "Todos" or x.ano == int(ano))
            and (tema == "Todos" or x.tema == tema)
            and (subtema == "Todos" or x.subtema == subtema)
            and (dif == "Todas" or x.dificuldade == dif))
results = [x for x in results if _keep(x)]

st.markdown(f"**{len(results)}** questão(ões) encontrada(s)")
PAGE = 10
page = st.number_input("Página", 1, max(1, -(-len(results) // PAGE)), 1) - 1
for questao in results[page * PAGE:(page + 1) * PAGE]:
    col1, col2 = st.columns([6, 1])
    with col2:
        is_fav = fav.is_fav(user, questao.id)
        if st.button("⭐" if is_fav else "☆", key=f"fav_{questao.id}",
                     help="Favoritar"):
            fav.toggle(user, questao.id)
            c["auth"].persist(user)
            st.rerun()
    with col1:
        question_full(questao)

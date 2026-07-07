"""Questões favoritadas pelo usuário."""
from __future__ import annotations

import streamlit as st

from components.question_card import question_full
from services.access_service import AccessService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "favoritas")

q, fav = c["questions"], c["favorites"]

st.markdown("## ⭐ Minhas favoritas")
st.caption("Questões que você marcou para rever depois.")

favs = q.get_many(user.favoritas)
if not favs:
    st.info("Nenhuma questão favoritada ainda. Marque com ⭐ na página **Praticar** ou **Questões**.")
    st.stop()

st.markdown(f"**{len(favs)}** questão(ões) favoritada(s).")
for questao in favs:
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️ Remover", key=f"unfav_{questao.id}"):
            fav.toggle(user, questao.id)
            c["auth"].persist(user)
            st.rerun()
    with col1:
        question_full(questao)

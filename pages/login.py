"""Tela de login."""
from __future__ import annotations

import streamlit as st

from components.ui import logo
from utils.context import ctx

c = ctx()
auth = c["auth"]

# Se o OAuth do Streamlit já autenticou, hidrata o perfil e segue.
if auth.hydrate_from_oauth():
    st.rerun()

_, mid, _ = st.columns([1, 1.2, 1])
with mid:
    st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
    logo()
    st.markdown("### Estude Física do jeito que ela merece: *cool*.")
    st.markdown(
        "Questões resolvidas de ENEM e vestibulares, simulados personalizados, "
        "XP por tema e uma trilha de cientistas para você desbloquear."
    )
    st.markdown("")
    if st.button("🔵 Entrar com Google", use_container_width=True, type="primary"):
        auth.login_google()
    if st.button("🧪 Entrar em modo demonstração", use_container_width=True):
        auth.login_demo()
        st.rerun()
    st.caption(f"Persistência: **{c['store'].backend}**"
               + (" (configure o Firebase no `.env` para produção)" if c['store'].backend == "local" else ""))

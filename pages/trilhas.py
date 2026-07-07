"""Trilhas de cientistas por tema (níveis e XP)."""
from __future__ import annotations

import streamlit as st

from components.ui import progress_bar, scientist_card
from config.settings import theme_meta
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
xp = c["xp"]

st.markdown("## 🧬 Trilhas de cientistas")
st.caption("Cada tema tem sua moeda de XP e sua linhagem de gênios para desbloquear.")

temas = sorted(set(list(user.xp_por_tema) + c["questions"].temas()))
tema = st.selectbox("Tema", temas, format_func=lambda t: f"{theme_meta(t)['icon']} {t}")

meta = theme_meta(tema)
pts = user.xp_por_tema.get(tema, 0)
info = xp.level_info(tema, pts)

st.markdown(f"### {meta['icon']} {tema} — {pts} {meta['moeda']}")
nxt = info["proximo"]
if nxt:
    st.caption(f"Nível {info['nivel']}/{info['total_niveis']} · próximo: **{nxt['nome']}** ({nxt['xp']} XP)")
else:
    st.caption("🏆 Trilha completa!")
progress_bar(info["progresso"], amber=True)
st.markdown("")

for sci in xp.track(tema):
    scientist_card(sci, unlocked=pts >= sci["xp"])

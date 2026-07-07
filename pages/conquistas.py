"""Galeria de conquistas (medalhas)."""
from __future__ import annotations

import streamlit as st

from services.access_service import AccessService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "conquistas")

ach = c["achievements"]

st.markdown("## 🏅 Conquistas")
todas = ach.all_with_state(user)
desbloqueadas = sum(1 for a in todas if a["unlocked"])
st.caption(f"{desbloqueadas}/{len(todas)} desbloqueadas")
st.progress(desbloqueadas / len(todas) if todas else 0)

cols = st.columns(3)
for i, a in enumerate(todas):
    with cols[i % 3]:
        if a["unlocked"]:
            st.markdown(
                f"""<div class="pc-card" style="text-align:center;margin-bottom:.7rem;
                    border-color:rgba(251,191,36,.5)">
                    <div style="font-size:2.4rem">{a['icon']}</div>
                    <div style="font-family:var(--font-display);font-weight:600">{a['nome']}</div>
                    <div style="font-size:.8rem;color:var(--ink-2)">{a['desc']}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                f"""<div class="pc-card" style="text-align:center;margin-bottom:.7rem;
                    opacity:.45;filter:grayscale(1)">
                    <div style="font-size:2.4rem">🔒</div>
                    <div style="font-family:var(--font-display);font-weight:600">{a['nome']}</div>
                    <div style="font-size:.8rem;color:var(--ink-2)">{a['desc']}</div>
                </div>""", unsafe_allow_html=True)

"""Prática avulsa: uma questão por vez com feedback imediato."""
from __future__ import annotations

import random

import streamlit as st

from components.question_card import question_header
from components.ui import achievement, badge, badges_row
from services.access_service import AccessService
from utils.context import ctx
from utils.latex import render_md
from services.ai_service import AIService

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "praticar")

q, practice, goals, fav = c["questions"], c["practice"], c["goals"], c["favorites"]

st.markdown("## 🎯 Praticar")
st.caption("Uma questão por vez, com correção na hora. Ótimo para treinar sem pressão.")

# meta diária no topo
gs = goals.status(user)
st.markdown(f"**Meta de hoje:** {gs['feitas']}/{gs['meta']} questões "
            + ("✅" if gs["cumprida"] else "🔥"))
st.progress(gs["progresso"])

# filtro opcional por tema
temas = st.multiselect("Filtrar por tema (opcional)", q.temas())
pool = q.filter(temas=temas) if temas else q.all()
if not pool:
    st.info("Sem questões para esse filtro.")
    st.stop()

# estado da questão atual na sessão
if "pc_pratica_id" not in st.session_state or st.session_state.get("pc_pratica_pool") != temas:
    st.session_state["pc_pratica_id"] = random.choice(pool).id
    st.session_state["pc_pratica_pool"] = temas
    st.session_state.pop("pc_pratica_resultado", None)

questao = q.get(st.session_state["pc_pratica_id"])
resultado = st.session_state.get("pc_pratica_resultado")

with st.container(border=True):
    top1, top2 = st.columns([4, 1])
    with top1:
        question_header(questao)
    with top2:
        is_fav = fav.is_fav(user, questao.id)
        if st.button("⭐ Favorita" if is_fav else "☆ Favoritar", use_container_width=True):
            fav.toggle(user, questao.id)
            c["auth"].persist(user)
            st.rerun()

    render_md(f"**{questao.enunciado}**")
    if questao.imagem:
        from config.settings import BASE_DIR
        st.image(questao.imagem if str(questao.imagem).startswith("http")
                 else str(BASE_DIR / questao.imagem))

    alts = questao.shuffled(seed=hash(questao.id) % 9999)
    disabled = resultado is not None
    escolha = st.radio("Alternativas", [a.id for a in alts],
                       format_func=lambda i: next(a.texto for a in alts if a.id == i),
                       index=None, disabled=disabled, label_visibility="collapsed",
                       key=f"radio_{questao.id}")

    if resultado is None:
        if st.button("Responder", type="primary", disabled=escolha is None):
            st.session_state["pc_pratica_resultado"] = practice.answer_single(questao, escolha)
            st.rerun()
    else:
        if resultado["acertou"]:
            st.success(f"✅ Correta! +{resultado['xp']} XP em {questao.tema}")
        else:
            st.error(f"❌ Incorreta. Resposta certa: **{resultado['correta_id']}**")
            tutor = AIService()
            if st.button("🤖 Por que errei? (tutor IA)"):
                with st.spinner("O tutor está analisando seu erro..."):
                    st.session_state["pc_tutor_txt"] = tutor.explain_mistake(questao, escolha)
            if "pc_tutor_txt" in st.session_state:
                with st.container(border=True):
                    render_md(st.session_state["pc_tutor_txt"])
        with st.expander("📝 Resolução", expanded=True):
            render_md(questao.resolucao or "_Sem resolução._")
        with st.expander("💡 Explicação conceitual"):
            render_md(questao.explicacao or "_Sem explicação._")

        for a in resultado.get("conquistas", []):
            achievement(a["nome"], a["desc"], "")
            st.balloons()

        if st.button("➡️ Próxima questão", type="primary"):
            st.session_state["pc_pratica_id"] = random.choice(pool).id
            st.session_state.pop("pc_pratica_resultado", None)
            st.session_state.pop("pc_tutor_txt", None)
            st.rerun()

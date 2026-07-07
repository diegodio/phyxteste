"""Revisão espaçada: questões que 'venceram' voltam para revisão."""
from __future__ import annotations

import streamlit as st

from components.question_card import question_header
from components.ui import metric_card
from services.access_service import AccessService
from utils.context import ctx
from utils.latex import render_md
from services.ai_service import AIService

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "revisar")

q, srs, practice = c["questions"], c["srs"], c["practice"]

st.markdown("## 🔁 Revisão de hoje")
st.caption("O sistema traz de volta questões que você já viu, no momento certo para fixar.")

counts = srs.counts(user)
cols = st.columns(3)
with cols[0]: metric_card("Para revisar hoje", str(counts["vencidas"]), "vencidas", "⏰")
with cols[1]: metric_card("Agendadas", str(counts["agendadas"]), "para os próximos dias", "📅")
with cols[2]: metric_card("Total no baralho", str(counts["total"]), "questões acompanhadas", "🗂️")

due_ids = srs.due(user)
if not due_ids:
    st.success("🎉 Nada para revisar agora! Volte amanhã ou faça novas questões em **Praticar**.")
    st.stop()

# questão atual da fila
if st.session_state.get("pc_rev_id") not in due_ids:
    st.session_state["pc_rev_id"] = due_ids[0]
    st.session_state.pop("pc_rev_resultado", None)

questao = q.get(st.session_state["pc_rev_id"])
if questao is None:  # questão removida do banco: descarta o card
    user.revisoes.pop(st.session_state["pc_rev_id"], None)
    c["auth"].persist(user)
    st.rerun()

resultado = st.session_state.get("pc_rev_resultado")
st.markdown(f"**{len(due_ids)}** questão(ões) na fila de hoje.")

with st.container(border=True):
    question_header(questao)
    render_md(f"**{questao.enunciado}**")
    if questao.imagem:
        from config.settings import BASE_DIR
        st.image(questao.imagem if str(questao.imagem).startswith("http")
                 else str(BASE_DIR / questao.imagem))

    alts = questao.shuffled(seed=hash(questao.id) % 9999)
    escolha = st.radio("Alternativas", [a.id for a in alts],
                       format_func=lambda i: next(a.texto for a in alts if a.id == i),
                       index=None, disabled=resultado is not None,
                       label_visibility="collapsed", key=f"rev_{questao.id}")

    if resultado is None:
        if st.button("Responder", type="primary", disabled=escolha is None):
            st.session_state["pc_rev_resultado"] = practice.answer_single(questao, escolha)
            st.rerun()
    else:
        card = user.revisoes.get(questao.id, {})
        if resultado["acertou"]:
            st.success(f"✅ Correta! Próxima revisão em {card.get('intervalo', 1)} dia(s).")
        else:
            st.error(f"❌ Errou — resposta certa: **{resultado['correta_id']}**. "
                     "Ela volta amanhã.")
            tutor = AIService()
            if st.button("🤖 Por que errei? (tutor IA)"):
                with st.spinner("O tutor está analisando seu erro..."):
                    st.session_state["pc_tutor_rev"] = tutor.explain_mistake(questao, escolha)
            if "pc_tutor_rev" in st.session_state:
                with st.container(border=True):
                    render_md(st.session_state["pc_tutor_rev"])
        with st.expander("📝 Resolução", expanded=True):
            render_md(questao.resolucao or "_Sem resolução._")
        if st.button("➡️ Próxima da fila", type="primary"):
            st.session_state.pop("pc_rev_id", None)
            st.session_state.pop("pc_rev_resultado", None)
            st.session_state.pop("pc_tutor_rev", None)
            st.rerun()

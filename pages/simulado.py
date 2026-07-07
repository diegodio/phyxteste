"""Mini simulados: configuração e execução."""
from __future__ import annotations

import streamlit as st

from components.question_card import question_header
from config.settings import (SIMULADO_FULL_SIZE, SIMULADO_FULL_TIMER,
                             SIMULADO_SIZE, TIMER_OPTIONS, theme_meta)
from utils.context import ctx
from utils.helpers import fmt_time

c = ctx()
q, sim = c["questions"], c["simulado"]
exam = sim.active()

# ---------------- configuração ----------------
if exam is None:
    st.markdown("## ⚡ Simulado")
    modo = st.radio("Formato", [f"Mini ({SIMULADO_SIZE} questões)",
                                f"Completo ({SIMULADO_FULL_SIZE} questões · 90 min)"],
                    horizontal=True)
    completo = modo.startswith("Completo")
    n = SIMULADO_FULL_SIZE if completo else SIMULADO_SIZE
    st.caption(f"{n} questões sorteadas, alternativas embaralhadas."
               + (" Treino de resistência no formato de prova real." if completo else ""))

    temas = st.multiselect("Escolha um ou mais temas", q.temas(),
                           format_func=lambda t: f"{theme_meta(t)['icon']} {t}")
    if completo:
        timer = SIMULADO_FULL_TIMER
        st.info("⏱️ Cronômetro fixo de **90 minutos**, como numa prova de verdade.")
    else:
        timer_label = st.select_slider("Cronômetro", list(TIMER_OPTIONS) + ["Personalizado"],
                                       value="Sem tempo")
        timer = TIMER_OPTIONS.get(timer_label, 0)
        if timer_label == "Personalizado":
            timer = st.number_input("Minutos", 1, 180, 25) * 60

    disponiveis = len(q.filter(temas=temas)) if temas else 0
    if temas and disponiveis < n:
        st.warning(f"Só há {disponiveis} questões para esses temas — "
                   f"o simulado sairá com esse total.")
    if st.button("🚀 Começar simulado", type="primary", disabled=not temas):
        if sim.start(temas, timer, n):
            st.rerun()
        else:
            st.warning("Não há questões para esses temas.")
    st.stop()

# ---------------- execução ----------------
questoes = exam["questoes"]
idx = exam["idx"]
qst = questoes[idx]

top1, top2 = st.columns([3, 1])
with top1:
    st.markdown(f"### Questão {idx + 1} / {len(questoes)}")
    st.progress((idx + 1) / len(questoes))
with top2:
    left = sim.time_left()
    if left is not None:
        st.markdown(f'<div class="pc-card" style="text-align:center">⏱️ <b>{fmt_time(left)}</b></div>',
                    unsafe_allow_html=True)
        if left <= 0:
            st.warning("Tempo esgotado! Finalizando…")
            sim.finish()
            st.switch_page("pages/resultado.py")

question_header(qst)
st.markdown(f"**{qst.enunciado}**")
if qst.imagem:
    from config.settings import BASE_DIR
    st.image(qst.imagem if str(qst.imagem).startswith("http") else str(BASE_DIR / qst.imagem))

alts = qst.shuffled(seed=exam["seeds"][qst.id])
current = exam["respostas"].get(qst.id)
labels = {a.id: f"{a.texto}" for a in alts}
choice = st.radio("Alternativas", [a.id for a in alts],
                  format_func=lambda i: labels[i],
                  index=[a.id for a in alts].index(current) if current else None,
                  label_visibility="collapsed")
if choice:
    sim.answer(qst.id, choice)

nav1, nav2, nav3 = st.columns([1, 1, 1])
with nav1:
    if st.button("← Anterior", disabled=idx == 0, use_container_width=True):
        exam["idx"] -= 1
        st.rerun()
with nav2:
    if idx < len(questoes) - 1:
        if st.button("Próxima →", use_container_width=True, type="primary"):
            exam["idx"] += 1
            st.rerun()
with nav3:
    respondidas = len(exam["respostas"])
    if st.button(f"✅ Finalizar ({respondidas}/{len(questoes)})", use_container_width=True,
                 type="primary" if idx == len(questoes) - 1 else "secondary"):
        sim.finish()
        st.switch_page("pages/resultado.py")

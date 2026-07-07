"""Página inicial (dashboard geral)."""
from __future__ import annotations

import streamlit as st

from components import charts
from components.ui import metric_card
from services.access_service import AccessService
from utils.context import ctx
from utils.helpers import fmt_time

c = ctx()
user = c["auth"].current_user()
q, stats, xp = c["questions"], c["stats"], c["xp"]
srs, goals = c["srs"], c["goals"]
AccessService.guard(user, "home")

st.markdown(f"## Olá, {user.nome.split()[0]} 👋")
st.caption("Seu laboratório de estudos, em tempo real.")

# ---- banco de questões ----
cols = st.columns(4)
with cols[0]: metric_card("Questões", str(len(q.all())), "no banco", "🧮")
with cols[1]: metric_card("Provas", str(len(q.provas())), "vestibulares e exames", "📄")
with cols[2]: metric_card("Anos", str(len(q.anos())), "edições disponíveis", "📅")
with cols[3]: metric_card("Temas", str(len(q.temas())), "áreas da Física", "⚛️")

st.markdown("")

# ---- desempenho pessoal ----
cols = st.columns(4)
with cols[0]: metric_card("XP total", f"{user.xp_total}", f"nível geral {xp.overall_level(user)}", "✨")
with cols[1]: metric_card("Taxa de acerto", f"{stats.accuracy(user):.0f}%", f"{user.questoes_respondidas} questões", "🎯")
with cols[2]: metric_card("Streak", f"{user.streak} 🔥", "dias seguidos de estudo", "")
with cols[3]: metric_card("Tempo estudado", fmt_time(user.tempo_estudado), "em simulados", "⏱️")

st.markdown("")

# --- revisão de hoje + meta diária ---
rc = srs.counts(user)
gs = goals.status(user)
cta1, cta2 = st.columns(2)
with cta1:
    st.markdown(f'''<div class="pc-card"><div class="pc-metric-label">🔁 Revisão de hoje</div>
        <div class="pc-metric-value">{rc["vencidas"]}</div>
        <div class="pc-metric-sub">questões esperando revisão</div></div>''',
        unsafe_allow_html=True)
with cta2:
    st.markdown(f'''<div class="pc-card"><div class="pc-metric-label">🎯 Meta diária</div>
        <div class="pc-metric-value">{gs["feitas"]}/{gs["meta"]}</div>
        <div class="pc-metric-sub">{"cumprida! ✅" if gs["cumprida"] else "questões hoje"}</div></div>''',
        unsafe_allow_html=True)

st.markdown("")

df = stats.exams_df(user)
left, right = st.columns([1.4, 1])
with left:
    if df.empty:
        st.info("Faça seu primeiro simulado para ver sua evolução aqui. ⚡")
    else:
        st.plotly_chart(charts.line(df, "data", "pct", "Evolução do desempenho (%)"),
                        use_container_width=True)
with right:
    st.markdown("#### Últimos simulados")
    if df.empty:
        st.caption("Nenhum simulado ainda.")
    else:
        for _, row in df.sort_values("data", ascending=False).head(5).iterrows():
            st.markdown(
                f"""<div class="pc-card" style="margin-bottom:.5rem">
                    <b>{row['acertos']}/{row['total']}</b> · {row['pct']:.0f}% ·
                    <span style="color:var(--ink-2)">{row['data'].strftime('%d/%m %H:%M')}</span><br>
                    <span style="color:var(--ink-2);font-size:.8rem">{', '.join(row['temas'])}</span>
                </div>""", unsafe_allow_html=True)

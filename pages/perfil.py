"""Perfil do usuário."""
from __future__ import annotations

import streamlit as st

from components import charts
from components.ui import metric_card, progress_bar
from config.settings import theme_meta
from services.export_service import ExportService
from utils.context import ctx
from utils.helpers import fmt_time

c = ctx()
user = c["auth"].current_user()
stats, xp = c["stats"], c["xp"]

col_a, col_b = st.columns([1, 3])
with col_a:
    if user.foto:
        st.image(user.foto, width=120)
with col_b:
    st.markdown(f"## {user.nome}")
    st.caption((user.email or "conta demo") + f" · nível geral **{xp.overall_level(user)}**")

cols = st.columns(4)
with cols[0]: metric_card("XP total", str(user.xp_total), "", "✨")
with cols[1]: metric_card("Streak", f"{user.streak} 🔥", "dias seguidos")
with cols[2]: metric_card("Simulados", str(len(user.simulados)), "", "⚡")
with cols[3]: metric_card("Tempo estudado", fmt_time(user.tempo_estudado), "", "⏱️")

pdf = ExportService.build_report(user, stats)
st.download_button("📄 Exportar relatório em PDF", data=pdf,
                   file_name=f"physicscool_{user.nome.split()[0].lower()}.pdf",
                   mime="application/pdf")

st.markdown("### ⚗️ XP por tema")
if not user.xp_por_tema:
    st.info("Responda simulados para acumular XP. ⚡")
for tema, pts in sorted(user.xp_por_tema.items(), key=lambda kv: -kv[1]):
    meta = theme_meta(tema)
    info = xp.level_info(tema, pts)
    nome = info["atual"]["nome"] if info["atual"] else "—"
    st.markdown(f"**{meta['icon']} {tema}** · {pts} {meta['moeda']} · nível {info['nivel']} ({nome})")
    progress_bar(info["progresso"])

st.markdown("### 🏅 Físicos desbloqueados")
unlocked = xp.unlocked(user)
if not unlocked:
    st.caption("Nenhum ainda — Tales de Mileto está esperando você.")
else:
    cols = st.columns(4)
    for i, (tema, sci) in enumerate(unlocked):
        with cols[i % 4]:
            st.markdown(
                f"""<div class="pc-card" style="text-align:center;margin-bottom:.6rem">
                    <img src="{sci['img']}" width="64" style="border-radius:50%;border:2px solid var(--photon)">
                    <div style="font-weight:600;font-family:var(--font-display)">{sci['nome']}</div>
                    <div style="font-size:.75rem;color:var(--ink-2)">{theme_meta(tema)['icon']} {tema}</div>
                </div>""", unsafe_allow_html=True)

df = stats.exams_df(user)
if not df.empty:
    st.plotly_chart(charts.line(df, "data", "pct", "Evolução do desempenho (%)"),
                    use_container_width=True)

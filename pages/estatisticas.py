"""Estatísticas completas."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from components import charts
from components.ui import metric_card
from utils.context import ctx
from utils.helpers import fmt_time

c = ctx()
user = c["auth"].current_user()
stats = c["stats"]

st.markdown("## 📊 Estatísticas")

df_ex = stats.exams_df(user)
df_ans = stats.answers_df(user)
if df_ex.empty:
    st.info("Sem dados ainda — faça um simulado. ⚡")
    st.stop()

cols = st.columns(4)
with cols[0]: metric_card("Taxa de acerto", f"{stats.accuracy(user):.0f}%", "", "🎯")
with cols[1]: metric_card("Questões", str(user.questoes_respondidas), "respondidas", "🧮")
with cols[2]: metric_card("Tempo médio", fmt_time(stats.avg_time_per_question(user)), "por questão", "⏱️")
strong, weak = stats.strongest_weakest(user)
with cols[3]: metric_card("Ponto forte", strong or "—", f"a revisar: {weak or '—'}", "💪")

periodo = st.radio("Período", ["Semanal", "Mensal", "Anual"], horizontal=True)
freq = {"Semanal": "W", "Mensal": "ME", "Anual": "YE"}[periodo]
serie = (df_ex.set_index("data")
              .resample(freq)
              .agg(pct=("pct", "mean"), questoes=("total", "sum"))
              .dropna().reset_index())

g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(charts.line(serie, "data", "pct", f"Desempenho {periodo.lower()} (%)"),
                    use_container_width=True)
with g2:
    st.plotly_chart(charts.bar(serie, "data", "questoes", "Questões respondidas",
                               charts.PHOTON), use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.plotly_chart(charts.bar(stats.by(user, "tema"), "tema", "pct",
                               "Desempenho por tema (%)"), use_container_width=True)
with g4:
    st.plotly_chart(charts.bar(stats.by(user, "prova"), "prova", "pct",
                               "Desempenho por vestibular (%)", charts.INDIGO),
                    use_container_width=True)

g5, g6 = st.columns(2)
with g5:
    st.plotly_chart(charts.bar(stats.by(user, "dificuldade"), "dificuldade", "pct",
                               "Por dificuldade (%)", charts.ION), use_container_width=True)
with g6:
    xp_df = pd.DataFrame([{"tema": t, "xp": v} for t, v in user.xp_por_tema.items()])
    if not xp_df.empty:
        st.plotly_chart(charts.pie(list(xp_df["tema"]), list(xp_df["xp"]),
                                   "Distribuição de XP"), use_container_width=True)

hab = stats.by_habilidade(user, c["questions"])
if not hab.empty:
    st.markdown("### 🧩 Desempenho por habilidade ENEM")
    st.plotly_chart(charts.bar(hab, "habilidade", "pct",
                               "Acerto por habilidade (%)", charts.INDIGO),
                    use_container_width=True)

st.markdown("### 🗂️ Histórico completo")
show = df_ex[["data", "temas", "acertos", "total", "pct", "tempo_gasto", "xp_ganho"]].copy()
show["temas"] = show["temas"].apply(", ".join)
show["tempo_gasto"] = show["tempo_gasto"].apply(fmt_time)
show.columns = ["Data", "Temas", "Acertos", "Total", "%", "Tempo", "XP"]
st.dataframe(show.sort_values("Data", ascending=False), use_container_width=True, hide_index=True)

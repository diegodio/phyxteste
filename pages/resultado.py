"""Dashboard de resultado do último simulado."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from components import charts
from components.question_card import question_full
from components.ui import achievement, metric_card
from utils.context import ctx
from utils.helpers import fmt_time

c = ctx()
user = c["auth"].current_user()
stats, xp = c["stats"], c["xp"]

result = st.session_state.get("pc_last_result")
questoes = st.session_state.get("pc_last_questions", [])

st.markdown("## 🏁 Resultado do simulado")
if result is None:
    st.info("Nenhum simulado finalizado nesta sessão. Faça um simulado primeiro. ⚡")
    st.stop()

# ---- conquista de nível ----
for tema in result.temas:
    info = xp.level_info(tema, user.xp_por_tema.get(tema, 0))
    prev = xp.level_info(tema, user.xp_por_tema.get(tema, 0) - result.xp_ganho)
    if info["nivel"] > prev["nivel"] and info["atual"]:
        sci = info["atual"]
        achievement(f"Nível {sci['nome']} desbloqueado!",
                    f"{tema} · {sci['contrib']}", sci["img"])
        st.balloons()

# ---- métricas ----
cols = st.columns(5)
with cols[0]: metric_card("Nota", f"{result.acertos}/{result.total}", f"{result.pct:.0f}%", "🎯")
with cols[1]: metric_card("Acertos", str(result.acertos), "", "✅")
with cols[2]: metric_card("Erros", str(result.total - result.acertos), "", "❌")
with cols[3]: metric_card("Tempo", fmt_time(result.tempo_gasto),
                          f"{fmt_time(result.tempo_gasto / result.total)}/questão", "⏱️")
with cols[4]: metric_card("XP ganho", f"+{result.xp_ganho}", "distribuído por tema", "✨")

st.markdown("")
df = pd.DataFrame(result.respostas)

# ---- gráficos ----
g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(charts.pie(["Acertos", "Erros"],
                               [result.acertos, result.total - result.acertos],
                               "Acertos × Erros"), use_container_width=True)
with g2:
    por_tema = df.groupby("tema")["acertou"].mean().mul(100).reset_index()
    if len(por_tema) >= 3:
        st.plotly_chart(charts.radar(list(por_tema["tema"]), list(por_tema["acertou"]),
                                     "Desempenho por tema (%)"), use_container_width=True)
    else:
        st.plotly_chart(charts.bar(por_tema, "tema", "acertou", "Desempenho por tema (%)"),
                        use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    por_dif = df.groupby("dificuldade")["acertou"].mean().mul(100).reset_index()
    st.plotly_chart(charts.bar(por_dif, "dificuldade", "acertou",
                               "Por dificuldade (%)", charts.PHOTON), use_container_width=True)
with g4:
    hist = stats.exams_df(user)
    st.plotly_chart(charts.line(hist, "data", "pct", "Evolução histórica (%)"),
                    use_container_width=True)

# ---- análise automática ----
st.markdown("### 🧠 Análise automática")
strong = df.groupby("tema")["acertou"].mean().sort_values(ascending=False)
msgs = [f"**Tema mais forte:** {strong.index[0]} ({strong.iloc[0]*100:.0f}%)",
        f"**Tema mais fraco:** {strong.index[-1]} ({strong.iloc[-1]*100:.0f}%) — vale uma revisão."]
if len(hist) >= 2:
    delta = hist.iloc[-1]["pct"] - hist.iloc[-2]["pct"]
    arrow = "📈 subiu" if delta >= 0 else "📉 caiu"
    msgs.append(f"**Comparado ao simulado anterior:** {arrow} {abs(delta):.0f} pontos percentuais.")
for m in msgs:
    st.markdown(f"- {m}")

# ---- revisão questão a questão ----
st.markdown("### 📚 Revisão das questões")
qmap = {q.id: q for q in questoes}
tab_ok, tab_bad = st.tabs([f"✅ Corretas ({result.acertos})",
                           f"❌ Incorretas ({result.total - result.acertos})"])
with tab_ok:
    for r in result.respostas:
        if r["acertou"] and r["question_id"] in qmap:
            question_full(qmap[r["question_id"]])
with tab_bad:
    for r in result.respostas:
        if not r["acertou"] and r["question_id"] in qmap:
            st.caption(f"Você marcou **{r['escolhida'] or '—'}** · correta: **{r['correta_id']}**")
            question_full(qmap[r["question_id"]])

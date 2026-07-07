"""Materiais de estudo (textos e vídeos) — PÁGINA PROTEGIDA.

A proteção anti-cópia/print/download vem de components/protection.py.
"""
from __future__ import annotations

import streamlit as st

from components.protection import content_protection
from components.ui import badge, badges_row
from config.settings import theme_meta
from services.access_service import AccessService
from services.material_service import MaterialService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()

# defesa em profundidade: bloqueia acesso direto por URL sem permissão
AccessService.guard(user, "materiais")

# 🔐 ativa TODAS as barreiras anti-reprodução nesta página
content_protection()

mats = MaterialService()

st.markdown("## 📚 Materiais de estudo")
st.caption("Textos e vídeos organizados por tema. Conteúdo protegido — uso pessoal.")

if not mats.all():
    st.info("Nenhum material cadastrado ainda. Adicione JSONs em `materials/<Tema>/`.")
    st.stop()

tema = st.selectbox("Tema", ["Todos"] + mats.temas(),
                    format_func=lambda t: t if t == "Todos" else f"{theme_meta(t)['icon']} {t}")
sel_tema = None if tema == "Todos" else tema

tab_txt, tab_vid = st.tabs(["📖 Textos", "🎬 Vídeos"])

_NIVEL = {"Básico": "green", "Intermediário": "amber", "Avançado": "rose"}

with tab_txt:
    textos = mats.by(tema=sel_tema, tipo="texto")
    if not textos:
        st.caption("Nenhum texto para esse filtro.")
    for m in textos:
        with st.container(border=True):
            meta = theme_meta(m.tema)
            badges_row(badge(f"{meta['icon']} {m.tema}"),
                       badge(m.nivel, _NIVEL.get(m.nivel, "")),
                       badge(f"✍️ {m.autor}", "slate") if m.autor else "")
            st.markdown(f"### {m.titulo}")
            st.caption(m.descricao)
            with st.expander("Ler material"):
                st.markdown(m.conteudo)

with tab_vid:
    videos = mats.by(tema=sel_tema, tipo="video")
    if not videos:
        st.caption("Nenhum vídeo para esse filtro.")
    for m in videos:
        with st.container(border=True):
            meta = theme_meta(m.tema)
            badges_row(badge(f"{meta['icon']} {m.tema}"),
                       badge(m.nivel, _NIVEL.get(m.nivel, "")))
            st.markdown(f"### {m.titulo}")
            st.caption(m.descricao)
            if "youtube.com" in m.video_url or "youtu.be" in m.video_url:
                st.video(m.video_url)
            else:
                # vídeo hospedado: player sem botão de download nem PiP
                st.markdown(
                    f'<video src="{m.video_url}" controls controlsList="nodownload noplaybackrate" '
                    f'disablepictureinpicture oncontextmenu="return false" '
                    f'style="width:100%;border-radius:14px"></video>',
                    unsafe_allow_html=True)

"""Physicscool — ponto de entrada e roteador.

physics school · physics is cool ⚛️

Fluxo de segurança (nesta ordem):
1. Login (Google ou demo)                       → services/auth_service.py
2. Allowlist de e-mails + LOGOUT AUTOMÁTICO     → config/access_control.py
3. Navegação montada só com páginas permitidas  → PAGE_PERMISSIONS
4. Ocultação do cromo do Streamlit              → styles/main.css (bloco final)
5. Proteção anti-cópia nos materiais            → components/protection.py
"""
from __future__ import annotations

import streamlit as st

from components.ui import inject_css, logo
from services.access_service import AccessService
from utils.context import ctx

st.set_page_config(page_title="Physicscool", page_icon="⚛️", layout="wide",
                   initial_sidebar_state="expanded")

inject_css(light=st.session_state.get("pc_light", False))

c = ctx()
auth = c["auth"]
user = auth.current_user() or auth.hydrate_from_oauth()

# ---- allowlist: quem não está na lista é deslogado na hora ----
if user is not None and not AccessService.enforce(user, auth):
    user = None

if user is None:
    if "pc_access_denied" in st.session_state:
        st.error(f"🚫 O e-mail **{st.session_state.pop('pc_access_denied')}** "
                 "não tem acesso ao Physicscool. Fale com o administrador.")
    login = st.Page("pages/login.py", title="Entrar", icon="🔐", default=True)
    st.navigation([login], position="hidden").run()
else:
    # ---- catálogo completo de páginas (chave → caminho, título, ícone) ----
    CATALOG: dict[str, tuple[str, str, str]] = {
        "home":         ("pages/home.py",         "Início",       "🏠"),
        "praticar":     ("pages/praticar.py",     "Praticar",     "🎯"),
        "revisar":      ("pages/revisar.py",      "Revisar",      "🔁"),
        "questoes":     ("pages/questoes.py",     "Questões",     "🔎"),
        "favoritas":    ("pages/favoritas.py",    "Favoritas",    "⭐"),
        "simulado":     ("pages/simulado.py",     "Simulado",     "⚡"),
        "resultado":    ("pages/resultado.py",    "Resultado",    "🏁"),
        "materiais":    ("pages/materiais.py",    "Materiais",    "📚"),
        "trilhas":      ("pages/trilhas.py",      "Trilhas",      "🧬"),
        "conquistas":   ("pages/conquistas.py",   "Conquistas",   "🏅"),
        "perfil":       ("pages/perfil.py",       "Perfil",       "👤"),
        "estatisticas": ("pages/estatisticas.py", "Estatísticas", "📊"),
        "professor":    ("pages/professor.py",    "Professor",    "🧑‍🏫"),
        "privacidade":  ("pages/privacidade.py",  "Privacidade",  "🔏"),
        "admin":        ("pages/admin.py",        "Admin",        "🛠️"),
    }

    # ---- monta a navegação apenas com o que o usuário pode ver ----
    allowed = AccessService.allowed_pages(user)
    visible = [(k, v) for k, v in CATALOG.items() if k in allowed]
    if not visible:  # allowlist ok mas sem nenhuma página: fallback seguro
        st.error("Sua conta não tem páginas liberadas. Fale com o administrador.")
        auth.logout()
        st.stop()
    pages = [st.Page(path, title=title, icon=icon, default=(i == 0))
             for i, (_, (path, title, icon)) in enumerate(visible)]

    with st.sidebar:
        logo(small=True)
        st.markdown("---")
    nav = st.navigation(pages)
    with st.sidebar:
        st.markdown("---")
        st.toggle("☀️ Tema claro", key="pc_light")
        st.caption(f"{'🧪 modo demo' if user.demo else user.email} · dados: {c['store'].backend}")
        if st.button("Sair", use_container_width=True):
            auth.logout()
            st.rerun()
    nav.run()

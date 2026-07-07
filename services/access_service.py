"""Aplicação das regras de config/access_control.py.

- `enforce(user, auth)`: derruba (logout automático) quem não está na allowlist.
- `allowed_pages(user)`: chaves de página que o usuário pode ver.
- `can(user, page_key)`: checagem pontual (defesa em profundidade dentro
  de páginas sensíveis, caso alguém acesse por URL direta).
"""
from __future__ import annotations

import streamlit as st

from config.access_control import is_email_allowed, pages_for
from models.user import User


class AccessService:
    @staticmethod
    def enforce(user: User, auth) -> bool:
        """True se o usuário pode permanecer logado; senão faz logout."""
        if is_email_allowed(user.email, demo=user.demo):
            return True
        auth.logout()
        st.session_state["pc_access_denied"] = user.email or "conta demo"
        return False

    @staticmethod
    def allowed_pages(user: User) -> set[str]:
        return pages_for(user.email, demo=user.demo)

    @classmethod
    def can(cls, user: User, page_key: str) -> bool:
        return page_key in cls.allowed_pages(user)

    @staticmethod
    def guard(user: User, page_key: str) -> None:
        """Chame no topo de uma página para bloquear acesso direto por URL."""
        if page_key not in pages_for(user.email, demo=user.demo):
            st.error("🔒 Você não tem permissão para acessar esta página.")
            st.stop()

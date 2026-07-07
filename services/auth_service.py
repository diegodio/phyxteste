"""Autenticação encapsulada.

- Google OAuth: usa `st.login()`/`st.user` (Streamlit >= 1.42) quando o OAuth
  estiver configurado em `.streamlit/secrets.toml` + Firebase Authentication.
- Modo demonstração: cria usuário temporário local imediatamente.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

import streamlit as st

from models.user import User
from services.storage_service import UserStore

_SESSION_KEY = "pc_user"


class AuthService:
    def __init__(self, store: UserStore) -> None:
        self._store = store

    # ---------- estado ----------
    def current_user(self) -> Optional[User]:
        return st.session_state.get(_SESSION_KEY)

    def _set(self, user: User) -> None:
        user.ultimo_acesso = datetime.now(timezone.utc).isoformat()
        st.session_state[_SESSION_KEY] = user
        self._store.save(user)

    # ---------- fluxos ----------
    def login_demo(self) -> User:
        uid = f"demo-{uuid.uuid4().hex[:8]}"
        user = User(uid=uid, nome="Explorador(a) Quântico(a)", demo=True,
                    foto="https://api.dicebear.com/9.x/bottts/svg?seed=" + uid)
        self._set(user)
        return user

    def login_google(self) -> None:
        """Dispara o OAuth nativo do Streamlit (requer secrets configurados)."""
        try:
            st.login("google")
        except Exception:
            st.error("OAuth Google não configurado. Adicione as credenciais em "
                     "`.streamlit/secrets.toml` (seção [auth]) — ou use o modo demonstração.")

    def hydrate_from_oauth(self) -> Optional[User]:
        """Se st.user tiver identidade Google, carrega/cria o perfil persistido."""
        info = getattr(st, "user", None)
        if not info or not getattr(info, "is_logged_in", False):
            return None
        email = getattr(info, "email", "") or ""
        uid = email or f"g-{uuid.uuid4().hex[:8]}"
        user = self._store.load(uid) or User(
            uid=uid, nome=getattr(info, "name", email) or email,
            email=email, foto=getattr(info, "picture", "") or "")
        self._set(user)
        return user

    def logout(self) -> None:
        st.session_state.pop(_SESSION_KEY, None)
        try:
            st.logout()
        except Exception:
            pass

    def persist(self, user: User) -> None:
        self._set(user)

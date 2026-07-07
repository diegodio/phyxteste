"""Privacidade e dados (LGPD): política, exportação e exclusão de conta."""
from __future__ import annotations

import json

import streamlit as st

from services.access_service import AccessService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "privacidade")

st.markdown("## 🔏 Privacidade e seus dados")

st.markdown("""
### Política de privacidade (resumo)

O **Physicscool** armazena apenas o necessário para o funcionamento da
plataforma: nome, e-mail, foto de perfil (vindos do login Google), seu
histórico de estudos (questões respondidas, simulados, XP, revisões) e
datas de acesso. **Não vendemos nem compartilhamos** seus dados com
terceiros. Os dados ficam no Firebase (Google Cloud) ou no servidor da
aplicação, conforme a configuração.

Em conformidade com a **LGPD (Lei 13.709/2018)**, você pode a qualquer
momento **exportar** uma cópia completa dos seus dados ou **excluir**
sua conta definitivamente — botões abaixo.
""")

st.markdown("### 📦 Exportar meus dados")
st.download_button(
    "⬇️ Baixar todos os meus dados (JSON)",
    data=json.dumps(user.to_dict(), ensure_ascii=False, indent=2),
    file_name=f"physicscool_dados_{user.uid}.json",
    mime="application/json",
)

st.markdown("### 🗑️ Excluir minha conta")
st.warning("A exclusão é **permanente**: todo o histórico, XP e conquistas "
           "serão apagados e você será deslogado.")
confirmar = st.text_input('Digite **EXCLUIR** para confirmar')
if st.button("Excluir minha conta definitivamente", type="primary",
             disabled=confirmar != "EXCLUIR"):
    c["store"].delete(user.uid)
    c["auth"].logout()
    st.success("Conta excluída. Até logo! 👋")
    st.rerun()

"""Painel administrativo: CRUD de questões e materiais, imagens e e-mails.

Acesso: permissão de página "admin" em config/access_control.py.
Persistência: Firestore quando há credenciais; senão, arquivos locais
(ver services/content_repository.py).
"""
from __future__ import annotations

import streamlit as st

from config.settings import THEME_XP
from services.access_service import AccessService
from services.admin_service import AdminService
from utils.context import ctx

c = ctx()
user = c["auth"].current_user()
AccessService.guard(user, "admin")

admin = AdminService()
q = c["questions"]
mats = c["materials"]

st.markdown("## 🛠️ Painel administrativo")
st.caption(f"Persistência de conteúdo: **{admin.backend}**")

tab_q, tab_gq, tab_m, tab_gm, tab_e = st.tabs(
    ["➕ Questão", "📋 Gerenciar questões", "📚 Material", "🗂️ Gerenciar materiais", "👥 E-mails"])

TEMAS = list(THEME_XP.keys())
NIVEIS = ["Básico", "Intermediário", "Avançado"]


def _question_form(prefill: dict | None = None, key: str = "nova") -> None:
    """Formulário de questão (criação ou edição via prefill)."""
    p = prefill or {}
    alts_pre = {a["id"]: a for a in p.get("alternativas", [])}
    with st.form(f"form_q_{key}", clear_on_submit=prefill is None):
        col1, col2, col3 = st.columns(3)
        prova = col1.text_input("Prova/Vestibular", p.get("prova", "ENEM"))
        ano = col2.number_input("Ano", 1990, 2100, p.get("ano", 2024))
        dif = col3.selectbox("Dificuldade", ["Fácil", "Média", "Difícil"],
                             index=["Fácil", "Média", "Difícil"].index(p.get("dificuldade", "Média")))
        col4, col5 = st.columns(2)
        tema = col4.selectbox("Tema", TEMAS,
                              index=TEMAS.index(p["tema"]) if p.get("tema") in TEMAS else 0)
        subtema = col5.text_input("Subtema", p.get("subtema", ""))
        qid = st.text_input("ID único", p.get("id", f"q{ano}xxx"),
                            disabled=prefill is not None)
        enunciado = st.text_area("Enunciado (aceita LaTeX $...$)",
                                 p.get("enunciado", ""), height=120)
        habilidades = st.text_input(
            "Habilidades ENEM (separadas por vírgula, ex.: H17, H21)",
            ", ".join(p.get("habilidades", [])))

        imagem_atual = p.get("imagem")
        if imagem_atual:
            st.caption(f"Imagem atual: `{imagem_atual}`")
        upload = st.file_uploader("Imagem da questão (opcional)",
                                  type=["png", "jpg", "jpeg", "webp"], key=f"img_{key}")

        st.markdown("**Alternativas** (marque a correta)")
        alts, corretas = [], []
        for letra in "ABCDE":
            ca, cb = st.columns([5, 1])
            pre = alts_pre.get(letra, {})
            txt = ca.text_input(f"Alternativa {letra}", pre.get("texto", ""),
                                key=f"alt_{key}_{letra}")
            ok = cb.checkbox("✔", pre.get("correta", False), key=f"ok_{key}_{letra}")
            alts.append((letra, txt)); corretas.append(ok)

        resolucao = st.text_area("Resolução completa", p.get("resolucao", ""), height=100)
        explicacao = st.text_area("Explicação conceitual", p.get("explicacao", ""), height=80)

        if st.form_submit_button("💾 Salvar questão", type="primary"):
            if not enunciado or not qid:
                st.error("Preencha ID e enunciado."); return
            if sum(corretas) != 1:
                st.error("Marque exatamente **uma** alternativa correta."); return
            if any(not t for _, t in alts):
                st.error("Preencha todas as 5 alternativas."); return
            imagem = imagem_atual
            if upload is not None:
                ext = upload.name.rsplit(".", 1)[-1]
                imagem = admin.save_image(upload.getvalue(), f"{qid}.{ext}")
            data = {
                "id": qid, "prova": prova, "ano": int(ano), "tema": tema,
                "subtema": subtema, "dificuldade": dif, "enunciado": enunciado,
                "alternativas": [{"id": l, "texto": t, "correta": corretas[i]}
                                 for i, (l, t) in enumerate(alts)],
                "resolucao": resolucao, "explicacao": explicacao,
                "habilidades": [h.strip().upper() for h in habilidades.split(",") if h.strip()],
                "tags": [tema.lower()], "fonte": prova, "imagem": imagem,
            }
            ref = admin.save_question(data)
            st.success(f"✅ Salvo em `{ref}`")


# ---------------- Criar questão ----------------
with tab_q:
    _question_form()

# ---------------- Gerenciar questões ----------------
with tab_gq:
    todas = q.all()
    if not todas:
        st.info("Nenhuma questão no banco.")
    else:
        alvo = st.selectbox("Questão", todas,
                            format_func=lambda x: f"{x.id} · {x.prova} {x.ano} · {x.tema}")
        col1, col2 = st.columns([1, 4])
        with col1:
            confirmar = st.checkbox("Confirmar exclusão")
            if st.button("🗑️ Excluir", disabled=not confirmar):
                admin.delete_question(alvo.id)
                st.success(f"Questão {alvo.id} excluída.")
                st.rerun()
        st.markdown("#### ✏️ Editar")
        raw = next(r for r in __import__("services.question_service",
                   fromlist=["_load_all"])._load_all() if r["id"] == alvo.id)
        _question_form(prefill=raw, key=f"edit_{alvo.id}")

# ---------------- Criar material ----------------
with tab_m:
    with st.form("novo_material", clear_on_submit=True):
        tipo = st.radio("Tipo", ["texto", "video"], horizontal=True)
        col1, col2 = st.columns(2)
        tema_m = col1.selectbox("Tema", TEMAS, key="tema_mat")
        nivel = col2.selectbox("Nível", NIVEIS)
        mid = st.text_input("ID único", "mat-xxx")
        titulo = st.text_input("Título")
        descricao = st.text_input("Descrição curta")
        autor = st.text_input("Autor (opcional)")
        conteudo = st.text_area("Conteúdo (Markdown + LaTeX) — só p/ texto", height=180)
        video_url = st.text_input("URL do vídeo — só p/ vídeo")
        if st.form_submit_button("💾 Salvar material", type="primary"):
            if not titulo or not mid:
                st.error("Preencha ID e título.")
            else:
                ref = admin.save_material({
                    "id": mid, "titulo": titulo, "tipo": tipo, "tema": tema_m,
                    "descricao": descricao, "conteudo": conteudo,
                    "video_url": video_url, "autor": autor, "nivel": nivel})
                st.success(f"✅ Salvo em `{ref}`")

# ---------------- Gerenciar materiais ----------------
with tab_gm:
    todos_m = mats.all()
    if not todos_m:
        st.info("Nenhum material cadastrado.")
    else:
        alvo_m = st.selectbox("Material", todos_m,
                              format_func=lambda m: f"{m.id} · {m.tema} · {m.titulo}")
        conf_m = st.checkbox("Confirmar exclusão do material")
        if st.button("🗑️ Excluir material", disabled=not conf_m):
            admin.delete_material(alvo_m.id)
            st.success(f"Material {alvo_m.id} excluído.")
            st.rerun()
        st.caption("Para editar, recrie com o mesmo ID na aba **📚 Material** "
                   "(o novo sobrescreve o antigo).")

# ---------------- E-mails ----------------
with tab_e:
    st.markdown("Adicione um e-mail à **allowlist** (`config/access_control.py`).")
    novo = st.text_input("E-mail")
    if st.button("Liberar acesso", type="primary"):
        if not novo or "@" not in novo:
            st.error("E-mail inválido.")
        elif AdminService.add_email(novo):
            st.success(f"✅ {novo} liberado (permissões padrão `_default`).")
        else:
            st.info("Esse e-mail já estava na lista.")
    st.caption("⚠️ Em deploy com filesystem efêmero, edite a allowlist no repositório "
               "e faça redeploy — a alteração via painel não sobrevive ao restart.")

# ⚛️ Physicscool

> *physics school* + *physics is cool*

Plataforma gamificada de estudos de Física para vestibulares (ENEM, FUVEST, UEL, UFPR, UNICAMP, ITA, IME...).

## Rodando

```bash
pip install -r requirements.txt
streamlit run app.py
```

Sem credenciais Firebase o app entra automaticamente em **modo local** (persistência em `.local_data/`) e o botão **"Entrar em modo demonstração"** cria um usuário temporário. Para produção, copie `.env.example` → `.env`, adicione o `serviceAccountKey.json` e configure OAuth Google (ver `services/auth_service.py`).

## Arquitetura

```
app.py               # roteador (st.navigation) + bootstrap
config/              # settings + credenciais centralizadas
models/              # dataclasses tipadas (Question, User, ExamResult)
services/            # auth, storage (Firebase c/ fallback local), questões, XP, simulados, stats
components/          # UI reutilizável (cards glass, badges, gráficos)
pages/               # telas
questions/PROVA/ANO/*.json   # banco de questões — leitura 100% dinâmica
styles/main.css      # identidade visual (tokens, glass, dark/light)
data/physicists.py   # trilhas de cientistas por tema
```

Adicionar provas/anos = criar pastas e soltar JSONs. Zero mudança de código.

## Identidade visual

Ver `BRAND.md`.

## 🔐 Controle de acesso

Tudo em **um único arquivo**: `config/access_control.py`
- `ALLOWED_EMAILS`: allowlist — e-mail fora da lista → **logout automático** (aplicado em `app.py` via `services/access_service.py`)
- `PAGE_PERMISSIONS`: páginas por e-mail (`"*"` = tudo; `_default` e `_demo` são fallbacks)
- Defesa em profundidade: páginas sensíveis chamam `AccessService.guard(user, "chave")`

## 📚 Materiais

`materials/<Tema>/*.json` (tipo `texto` ou `video`) — leitura dinâmica, igual às questões. Ver formato em `services/material_service.py`.

## 🛡️ Proteção de conteúdo

- **Anti-cópia/print/download**: `components/protection.py` (CSS + JS documentados no topo do arquivo). Ativado em `pages/materiais.py` via `content_protection()`.
- **Ocultação do cromo do Streamlit** (menu, footer, deploy, GitHub): bloco final de `styles/main.css`, marcado com o comentário "OCULTAÇÃO DOS VESTÍGIOS DO STREAMLIT".

> Nota: proteção client-side é dissuasão em camadas — nenhum front-end impede 100% (ex.: foto do celular).

## 🆕 Recursos de estudo

- **🎯 Praticar** (`pages/praticar.py`): questão avulsa com correção imediata, LaTeX, favoritar. Toda resposta passa por `services/practice_service.py`, que dispara XP + SRS + meta + conquistas de forma consistente.
- **🔁 Revisar** (`pages/revisar.py`): revisão espaçada (SM-2) — `services/srs_service.py`. Errou volta amanhã; acertos aumentam o intervalo.
- **⭐ Favoritas** (`pages/favoritas.py` + `services/favorite_service.py`): usa o campo `user.favoritas`.
- **🏅 Conquistas** (`pages/conquistas.py`): catálogo editável em `data/achievements.py`; avaliação em `services/achievement_service.py`.
- **🎯 Metas diárias** (`services/goal_service.py`): reinicia por dia; editar `DEFAULT_META`.
- **🔍 Busca textual**: `QuestionService.search()`; caixa de busca em Questões.
- **🧮 LaTeX**: escreva `$F = ma$` nos JSON; render em `utils/latex.py`.
- **📄 Export PDF** (`services/export_service.py`): botão no Perfil, sem dependências externas.

## 🛠️ Painel admin

`pages/admin.py` + `services/admin_service.py` — cadastra questões e materiais por formulário e adiciona e-mails à allowlist. Só acessível a quem tem a página `admin` (ou `"*"`) em `PAGE_PERMISSIONS`.

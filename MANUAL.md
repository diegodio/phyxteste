# 📖 Manual do Physicscool

> Documentação completa de todas as funcionalidades. Última atualização: julho/2026.

---

## 1. Visão geral

O **Physicscool** (*physics school* + *physics is cool*) é uma plataforma gamificada de estudos de Física para ENEM e vestibulares. Roda em Streamlit, persiste no Firebase (ou localmente, sem credenciais) e inclui tutor com IA via modelos hospedados pela NVIDIA.

**Como rodar:** `pip install -r requirements.txt && streamlit run app.py`

---

## 2. Páginas do site

### 🏠 Início
Dashboard geral: total de questões/provas/temas do banco, XP, nível, streak, taxa de acerto, tempo estudado, cartões de **revisão de hoje** e **meta diária**, gráfico de evolução e últimos simulados.

### 🎯 Praticar
Uma questão por vez com **correção imediata**. Filtro opcional por tema, barra da meta diária no topo, botão ⭐ favoritar. Ao errar, aparece o botão **🤖 Por que errei?** — o tutor IA analisa o erro específico. Cada resposta alimenta automaticamente: XP do tema, revisão espaçada, meta diária e conquistas.

### 🔁 Revisar
**Revisão espaçada (algoritmo SM-2).** Toda questão respondida vira um "card": errou → volta amanhã; acertos consecutivos → intervalo cresce (1 → 3 → ~8 dias...). A página mostra só o que "venceu" hoje, com contadores (vencidas / agendadas / total).

### 🔎 Questões
Banco completo com **busca textual** (palavra no enunciado, tema, tags) + filtros por vestibular, ano, tema, subtema e dificuldade. Cada questão mostra resolução completa e explicação conceitual. Botão ⭐ para favoritar. Paginação de 10 em 10.

### ⭐ Favoritas
Lista das questões marcadas, com botão para remover.

### ⚡ Simulado
Dois formatos:
- **Mini**: 10 questões, cronômetro livre (sem tempo, 5–30 min ou personalizado)
- **Completo**: 45 questões com cronômetro fixo de 90 min (formato prova real)

Questões sorteadas, alternativas embaralhadas, navegação entre questões, finalização a qualquer momento.

### 🏁 Resultado
Dashboard pós-simulado: nota, %, tempo total e por questão, acertos/erros, XP ganho. Gráficos: pizza, radar por tema, barras por dificuldade, evolução histórica. **Análise automática** (tema forte/fraco, comparação com o anterior). Revisão questão a questão em abas Corretas/Incorretas. Animação de conquista ao subir de nível.

### 📚 Materiais
Textos e vídeos por tema, em abas, com badges de nível (Básico/Intermediário/Avançado). **Página protegida** contra cópia/print/download (ver seção 6).

### 🧬 Trilhas
Trilha de cientistas por tema (Tales → Tesla na Eletricidade, etc.). Cada cientista tem bio, contribuição e XP para desbloqueio, com barra de progresso.

### 🏅 Conquistas
Galeria de medalhas (10 no catálogo): primeira questão, 100 questões, streaks, XP acumulado, gabaritar simulado... Desbloqueadas ficam douradas; travadas, em cinza.

### 👤 Perfil
Foto, nome, nível geral, métricas, XP por tema com barras, físicos desbloqueados, gráfico de evolução e botão **📄 Exportar relatório em PDF**.

### 📊 Estatísticas
Evolução semanal/mensal/anual, questões por período, desempenho por tema/vestibular/dificuldade, **desempenho por habilidade ENEM** (H17, H21...), distribuição de XP e histórico completo em tabela.

### 🧑‍🏫 Professor
Visão da turma (todos os usuários não-demo): métricas agregadas, **alunos em risco** (inativos 7+ dias, streak zerado, acerto <50%), gráfico de **onde a turma mais erra** por tema, e ranking de XP.

### 🔏 Privacidade
Política de privacidade resumida + direitos LGPD: **exportar todos os dados** (JSON) e **excluir a conta** definitivamente (com confirmação digitada).

### 🛠️ Admin
CRUD completo sem editar arquivos:
- **➕ Questão**: formulário com LaTeX, habilidades ENEM, upload de imagem, validação (exatamente 1 correta)
- **📋 Gerenciar questões**: editar (formulário pré-preenchido) e excluir (com confirmação)
- **📚 Material** / **🗂️ Gerenciar materiais**: criar, sobrescrever por ID, excluir
- **👥 E-mails**: adicionar à allowlist

---

## 3. Gamificação

| Tema | Moeda de XP |
|---|---|
| Mecânica | ⚙️ Engrenagens |
| Eletricidade | ⚡ Raios |
| Magnetismo | 🧲 Ímãs |
| Hidrostática | 💧 Gotas |
| Ondulatória | 🌊 Ondas |
| Termologia | 🔥 Chamas |
| Óptica | 🔍 Lentes |
| Astronomia | 🌌 Estrelas |

- Acerto = **15 XP** no tema da questão (+5 de bônus por acerto em sequência no simulado) — valores em `config/settings.py`
- Níveis = cientistas da trilha do tema (`data/physicists.py`)
- Streak = dias consecutivos com atividade
- Meta diária = 10 questões (editável em `services/goal_service.py` → `DEFAULT_META`)

---

## 4. Controle de acesso

Tudo em **`config/access_control.py`**:
- `ALLOWED_EMAILS`: quem pode logar; e-mail fora da lista → **logout automático**
- `PAGE_PERMISSIONS`: páginas por e-mail (`"*"` = todas; `_default`/`_demo` = fallbacks)
- `ALLOW_DEMO`: liga/desliga o botão de demonstração

Chaves de página: `home, praticar, revisar, questoes, favoritas, simulado, resultado, materiais, trilhas, conquistas, perfil, estatisticas, professor, privacidade, admin`.

Cada página sensível também chama `AccessService.guard()` no topo (defesa em profundidade contra URL direta).

---

## 5. Tutor IA (NVIDIA)

- Configuração: `config/ai_config.py` — precisa de `NVIDIA_API_KEY` no `.env` (chave gratuita em https://build.nvidia.com)
- Serviço: `services/ai_service.py` — endpoint NIM compatível com OpenAI
- Onde aparece: botão "🤖 Por que errei?" nas correções de **Praticar** e **Revisar**
- Sem chave: o botão mostra aviso amigável; nada quebra
- Trocar de modelo: variável `NVIDIA_MODEL` no `.env`

---

## 6. Proteção de conteúdo

- **`components/protection.py`** (documentado no cabeçalho): bloqueia seleção/cópia, botão direito, Ctrl+C/X/S/P/U/A, F12/devtools; PrintScreen limpa clipboard e cobre a tela; perda de foco borra o conteúdo; Ctrl+P imprime em branco. Ativo na página **Materiais**.
- **`styles/main.css`** (bloco final "OCULTAÇÃO DOS VESTÍGIOS DO STREAMLIT"): esconde menu, footer, Deploy, GitHub.
- ⚠️ Dissuasão, não blindagem: foto de celular sempre passa. Atenção: prejudica leitores de tela (acessibilidade).

---

## 7. Armazenamento

| Dado | Com Firebase | Sem Firebase |
|---|---|---|
| Usuários | Firestore `users/` | `.local_data/user_*.json` |
| Questões (admin) | Firestore `questions/` | `questions/PROVA/ANO/*.json` |
| Materiais (admin) | Firestore `materials/` | `materials/Tema/*.json` |
| Imagens | Storage (`FIREBASE_STORAGE_BUCKET`) | `assets/uploads/` |

A leitura **sempre mescla** disco + Firestore (id repetido: Firestore vence). Detecção automática: basta existir o arquivo de credenciais apontado no `.env`. Código: `services/content_repository.py` e `services/storage_service.py`.

---

## 8. Conteúdo: formatos dos JSON

**Questão** (`questions/PROVA/ANO/id.json`): campos `id, prova, ano, tema, subtema, dificuldade, enunciado, alternativas[{id,texto,correta}], resolucao, explicacao, habilidades[], tags[], fonte, imagem`. LaTeX entre `$...$`.

**Material** (`materials/Tema/id.json`): `id, titulo, tipo("texto"|"video"), tema, descricao, conteudo(markdown), video_url, autor, nivel`.

---

## 9. Testes

```bash
pytest tests/ -v
```
21 testes cobrindo SRS, XP/níveis, metas, conquistas, favoritos, modelo de questão, PDF e controle de acesso.

---

## 10. Mapa de arquivos

```
app.py                     roteador + allowlist + navegação por permissão
config/
  settings.py              constantes (XP, tamanhos de simulado, temas)
  access_control.py        ★ allowlist + permissões por página
  firebase_config.py       ★ credenciais Firebase centralizadas
  ai_config.py             ★ credenciais NVIDIA
models/                    Question, User, ExamResult (dataclasses)
services/
  auth_service.py          login Google + demo + sessão
  storage_service.py       usuários (Firestore/local) + list/delete
  content_repository.py    questões/materiais (Firestore/disco) + imagens
  question_service.py      leitura, filtros, busca, sorteio
  material_service.py      leitura de materiais
  simulado_service.py      ciclo de vida do simulado
  practice_service.py      resposta avulsa (dispara XP+SRS+meta+conquistas)
  srs_service.py           revisão espaçada SM-2
  xp_service.py            XP e níveis por trilha
  goal_service.py          metas diárias
  achievement_service.py   medalhas
  favorite_service.py      favoritos
  stats_service.py         agregações (inclui por habilidade ENEM)
  teacher_service.py       visões de turma
  ai_service.py            tutor NVIDIA
  export_service.py        PDF sem dependências
  admin_service.py         CRUD via repositório
  access_service.py        enforcement da allowlist/permissões
components/                ui.py, question_card.py, charts.py, protection.py
pages/                     uma página por arquivo
data/                      physicists.py (trilhas), achievements.py (medalhas)
questions/, materials/     conteúdo seed em JSON
styles/main.css            identidade visual + ocultação do Streamlit
tests/test_core.py         suíte pytest
```

★ = únicos lugares com credenciais/controle de acesso.

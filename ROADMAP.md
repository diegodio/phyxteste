# 🗺️ Roadmap — próximos passos e melhorias

Ordenado por prioridade sugerida.

## Curto prazo (alto valor, baixo esforço)

1. **Ranking entre alunos** — página de leaderboard (XP semanal/geral). Os dados já existem; é uma query ordenada em `UserStore.list_users()`. Só faz sentido com vários alunos reais logando.
2. **Permissões editáveis pelo admin** — hoje `PAGE_PERMISSIONS` se edita no código; mover para Firestore permitiria gerenciar tudo pelo painel (e sobreviver a redeploys).
3. **Notificações de revisão** — e-mail ou WhatsApp diário "você tem N questões para revisar" (integração natural com seu know-how de ENEMZap).
4. **Dica de estudo por IA no Resultado** — `AIService.study_tip()` já existe; falta chamar na tela de resultado para o tema mais fraco.
5. **Seed maior de questões** — o sistema aguenta milhares; o gargalo agora é conteúdo. Um script de importação em lote (CSV → JSON) aceleraria muito.

## Médio prazo

6. **Turmas/grupos** — professor cria turma com código de convite; painel do professor filtra por turma. Requer campo `turma` no User + tela de entrada de código.
7. **Modo offline/PWA** — cache das questões para estudar sem internet (você já fez PWA no Geringonça).
8. **Explicações em vídeo por questão** — campo `video_resolucao` no JSON, player embutido na correção.
9. **Migração de imagens para Firebase Storage com URLs assinadas** — hoje `make_public()`; URLs assinadas com expiração protegem melhor o conteúdo.
10. **Acessibilidade da proteção de conteúdo** — oferecer um "modo acessível" por usuário (permissão) que desativa `user-select:none` e bloqueios de teclado para quem usa leitor de tela.

## Longo prazo

11. **Streaming de vídeo com DRM/token** — proteção real de vídeos (a atual é dissuasão client-side).
12. **App mobile** (Streamlit é responsivo, mas um wrapper PWA instalável melhora retenção).
13. **Geração de questões por IA com revisão humana** — o tutor NVIDIA pode rascunhar questões novas por tema/habilidade; o admin aprova antes de publicar.
14. **Analytics de aprendizado** — curva de esquecimento real por aluno, previsão de nota ENEM por regressão sobre o histórico.
15. **Multi-disciplina** — a arquitetura (temas → trilhas → XP) é agnóstica; Química e Matemática entrariam só com novos dados em `data/` e `questions/`.

## Dívidas técnicas conhecidas

- `AdminService.add_email` edita arquivo de código: não sobrevive a filesystem efêmero (mover allowlist para Firestore — item 2).
- Testes cobrem serviços, não páginas (adicionar testes de UI com `streamlit.testing.v1.AppTest`).
- `st.cache_data` sem TTL: em multiusuário com Firestore, adicionar `ttl=300` para conteúdo novo aparecer sem redeploy.
- O modo demonstração cria arquivos/documentos de usuário a cada clique; adicionar limpeza periódica de contas `demo-*` antigas.

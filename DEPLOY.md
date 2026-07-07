# 🚀 Guia de deploy — colocando o Physicscool no ar

Passo a passo do zero até produção, incluindo todas as credenciais.

---

## Parte A — Rodar localmente (5 min)

```bash
cd physicscool
pip install -r requirements.txt
streamlit run app.py
```
Abra http://localhost:8501 e clique em **"Entrar em modo demonstração"**. Sem nenhuma credencial, tudo funciona em modo local (dados em `.local_data/`).

---

## Parte B — Firebase (persistência em produção)

1. Acesse https://console.firebase.google.com → **Adicionar projeto** (ex.: `physicscool`).
2. No projeto: **Criação (Build) → Firestore Database → Criar banco** → modo produção → região `southamerica-east1` (São Paulo).
3. **Configurações do projeto (⚙️) → Contas de serviço → Gerar nova chave privada** → baixa um JSON.
4. Salve o JSON como `config/serviceAccountKey.json` (⚠️ **nunca** comite no Git — adicione ao `.gitignore`).
5. Copie `.env.example` para `.env` e preencha:
   ```
   FIREBASE_CREDENTIALS_PATH=config/serviceAccountKey.json
   ```
6. (Opcional, para imagens) **Build → Storage → Começar** e adicione ao `.env`:
   ```
   FIREBASE_STORAGE_BUCKET=physicscool.appspot.com
   ```
7. Reinicie o app. A sidebar deve mostrar `dados: firebase`. A partir daí, usuários, questões e materiais criados pelo admin vão para o Firestore automaticamente.

---

## Parte C — Login com Google (OAuth)

1. https://console.cloud.google.com → selecione o MESMO projeto do Firebase.
2. **APIs e serviços → Tela de consentimento OAuth** → tipo Externo → preencha nome do app e e-mail.
3. **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth** → tipo "Aplicativo da Web".
4. Em **URIs de redirecionamento autorizados**, adicione:
   - Local: `http://localhost:8501/oauth2callback`
   - Produção: `https://SEU-DOMINIO/oauth2callback`
5. Copie o **Client ID** e o **Client Secret**.
6. Crie `.streamlit/secrets.toml`:
   ```toml
   [auth]
   redirect_uri = "https://SEU-DOMINIO/oauth2callback"
   cookie_secret = "uma-string-aleatoria-longa-qualquer"
   client_id = "SEU_CLIENT_ID.apps.googleusercontent.com"
   client_secret = "SEU_CLIENT_SECRET"
   server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
   ```
7. Instale a dependência de auth: `pip install "streamlit[auth]"` (Authlib).
8. Teste o botão **"Entrar com Google"**. Lembre-se: o e-mail precisa estar em `ALLOWED_EMAILS` (`config/access_control.py`), senão o logout é automático.

---

## Parte D — Tutor IA (NVIDIA)

1. Acesse https://build.nvidia.com e crie uma conta (gratuita, com créditos de API).
2. Escolha um modelo (ex.: `meta/llama-3.3-70b-instruct`) → **Get API Key**.
3. Adicione ao `.env`:
   ```
   NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxx
   NVIDIA_MODEL=meta/llama-3.3-70b-instruct
   ```
4. Reinicie. O botão "🤖 Por que errei?" passa a responder de verdade.

---

## Parte E — Publicar na internet

### Opção 1: Streamlit Community Cloud (grátis, mais simples)
1. Suba o projeto para um repositório **privado** no GitHub (confira que `.env`, `serviceAccountKey.json` e `.local_data/` estão no `.gitignore`).
2. https://share.streamlit.io → **New app** → aponte para o repo e `app.py`.
3. Em **Settings → Secrets**, cole o conteúdo do `secrets.toml` E as variáveis do `.env` (o Streamlit Cloud lê ambos de lá). Para a credencial Firebase, cole o JSON inteiro como um secret e ajuste `firebase_config.py` para lê-lo de `st.secrets` se preferir (ou use o caminho de arquivo com o JSON comitado — **não recomendado**).
4. ⚠️ Filesystem é efêmero: com o Firebase configurado (Parte B) isso não é problema — conteúdo e usuários vivem no Firestore.

### Opção 2: VPS (Hostinger, DigitalOcean, Oracle Free Tier...)
```bash
# no servidor (Ubuntu)
sudo apt update && sudo apt install python3-pip python3-venv nginx -y
git clone SEU_REPO && cd physicscool
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt "streamlit[auth]"
# suba o .env e o serviceAccountKey.json por scp (fora do git)
streamlit run app.py --server.port 8501 --server.headless true
```
Depois configure o nginx como proxy reverso para a porta 8501 e HTTPS com certbot (`sudo certbot --nginx -d seudominio.com`). Para manter o app vivo, crie um serviço systemd.

---

## Parte F — Checklist final antes de liberar para alunos

- [ ] `ALLOWED_EMAILS` com os e-mails reais; remova os de exemplo
- [ ] `PAGE_PERMISSIONS`: defina quem é admin (`"*"`), quem é professor, e o `_default` dos alunos
- [ ] `ALLOW_DEMO = False` se não quiser contas anônimas em produção
- [ ] Firestore em modo produção com regras restritas (o acesso é só via conta de serviço, então as regras podem negar tudo para clientes: `allow read, write: if false;`)
- [ ] Teste o fluxo completo: login → praticar → errar → tutor IA → revisar no dia seguinte
- [ ] Rode `pytest tests/ -v` (21 testes devem passar)
- [ ] Faça um backup/export inicial do Firestore configurado

"""=====================================================================
PROTEÇÃO DE CONTEÚDO (anti-cópia / anti-print / anti-download)
=====================================================================
👉 ESTE é o arquivo que dificulta a reprodução do conteúdo. <<<<<<<<<<

Chame `content_protection()` no topo de qualquer página protegida
(hoje: pages/materiais.py). As barreiras aplicadas:

  CSS
  • user-select:none em tudo (impede selecionar/copiar texto)
  • @media print { visibility:hidden } (Ctrl+P sai em branco)
  • pointer-events/drag bloqueados em imagens (impede arrastar/salvar)
  • vídeos com controlsList="nodownload" + sem picture-in-picture

  JavaScript (injetado no documento pai)
  • bloqueia menu de contexto (botão direito)
  • bloqueia eventos copy / cut / dragstart / selectstart
  • bloqueia atalhos: Ctrl/Cmd + C, X, S, P, U, A e Ctrl+Shift+I/J/C (devtools)
  • tecla PrintScreen → limpa a área de transferência e cobre a tela
    com um véu por 1,5 s (o print sai coberto)
  • ao perder o foco da janela (troca p/ ferramenta de captura),
    aplica blur no conteúdo até o foco voltar

⚠️ Honestidade técnica: nada disso é inviolável — front-end não impede
foto de celular nem usuário avançado. É dissuasão em camadas.
=====================================================================
"""
from __future__ import annotations

import streamlit.components.v1 as components
import streamlit as st

_PROTECT_CSS = """
<style id="pc-protect">
/* ---- seleção e cópia ---- */
.stApp, .stApp * {
  -webkit-user-select:none !important; -moz-user-select:none !important;
  user-select:none !important;
  -webkit-touch-callout:none !important;
}
/* ---- impressão sai em branco ---- */
@media print { body * { visibility:hidden !important; } body:after{
  content:"Conteúdo protegido — Physicscool"; visibility:visible;
  position:fixed; top:40%; left:0; right:0; text-align:center; } }
/* ---- imagens: sem arrastar/salvar ---- */
img { pointer-events:none !important; -webkit-user-drag:none !important; user-drag:none !important; }
/* ---- véu anti-printscreen (ativado via JS) ---- */
#pc-veil { position:fixed; inset:0; background:#0B1120; z-index:999999;
  display:none; align-items:center; justify-content:center;
  color:#22D3EE; font-family:sans-serif; font-size:1.2rem; }
#pc-veil.on { display:flex; }
.pc-blurred .stApp{ filter:blur(14px) !important; }
</style>
<div id="pc-veil">⚛️ Conteúdo protegido</div>
"""

_PROTECT_JS = """
<script>
(function () {
  // roda no documento PAI (a página do app), não no iframe do componente
  const doc = window.parent.document;
  if (doc.getElementById('pc-protect-js')) return;   // evita duplicar
  const mark = doc.createElement('meta'); mark.id = 'pc-protect-js';
  doc.head.appendChild(mark);

  const kill = e => { e.preventDefault(); e.stopPropagation(); return false; };

  // botão direito, cópia, recorte, arrastar, selecionar
  ['contextmenu','copy','cut','dragstart','selectstart'].forEach(
    ev => doc.addEventListener(ev, kill, {capture:true})
  );

  // atalhos de teclado
  doc.addEventListener('keydown', function (e) {
    const k = e.key.toLowerCase();
    const combo = e.ctrlKey || e.metaKey;
    if (combo && ['c','x','s','p','u','a'].includes(k)) return kill(e);
    if (combo && e.shiftKey && ['i','j','c'].includes(k)) return kill(e); // devtools
    if (e.key === 'F12') return kill(e);
    if (e.key === 'PrintScreen') {
      try { navigator.clipboard.writeText(''); } catch (_) {}
      veil(1500);
      return kill(e);
    }
  }, {capture:true});

  // véu que cobre a tela
  function veil(ms) {
    const v = doc.getElementById('pc-veil');
    if (!v) return;
    v.classList.add('on');
    setTimeout(() => v.classList.remove('on'), ms);
  }

  // perda de foco (ferramentas de captura) → borra o app
  window.parent.addEventListener('blur',  () => doc.body.classList.add('pc-blurred'));
  window.parent.addEventListener('focus', () => doc.body.classList.remove('pc-blurred'));
})();
</script>
"""


def content_protection() -> None:
    """Ativa todas as barreiras anti-reprodução na página atual."""
    st.markdown(_PROTECT_CSS, unsafe_allow_html=True)
    components.html(_PROTECT_JS, height=0, width=0)

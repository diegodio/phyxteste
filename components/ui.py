"""Componentes visuais reutilizáveis do Physicscool."""
from __future__ import annotations

import streamlit as st

from config.settings import APP_TAGLINE, STYLES_DIR


def inject_css(light: bool = False) -> None:
    css = (STYLES_DIR / "main.css").read_text(encoding="utf-8")
    theme = '<script>document.body.dataset.pcTheme="light";</script>' if light else ""
    st.markdown(f"<style>{css}</style>{theme}", unsafe_allow_html=True)
    if light:
        st.markdown("<style>html,body,.stApp{--void:#F6F8FC;--deep:#FFF;--surface:#FFF;"
                    "--glass:rgba(11,17,32,.04);--stroke:rgba(11,17,32,.12);"
                    "--ink:#0B1120;--ink-2:#5B6B84;}</style>", unsafe_allow_html=True)


def logo(small: bool = False) -> None:
    size = "1.15rem" if small else "1.6rem"
    st.markdown(
        f'<div class="pc-logo" style="font-size:{size}">Physicsc<span class="oo">⚛o</span>l</div>'
        f'<div class="pc-tagline">{APP_TAGLINE}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, sub: str = "", icon: str = "") -> None:
    st.markdown(
        f'''<div class="pc-card pc-fade">
              <div class="pc-metric-label">{icon} {label}</div>
              <div class="pc-metric-value">{value}</div>
              <div class="pc-metric-sub">{sub}</div>
            </div>''',
        unsafe_allow_html=True,
    )


def badge(text: str, kind: str = "") -> str:
    return f'<span class="pc-badge {kind}">{text}</span>'


def badges_row(*items: str) -> None:
    st.markdown('<div style="display:flex;gap:.4rem;flex-wrap:wrap">' + "".join(items) + "</div>",
                unsafe_allow_html=True)


def progress_bar(pct: float, amber: bool = False) -> None:
    cls = "pc-bar amber" if amber else "pc-bar"
    st.markdown(f'<div class="{cls}"><span style="width:{pct*100:.1f}%"></span></div>',
                unsafe_allow_html=True)


def achievement(title: str, subtitle: str, img: str = "") -> None:
    img_html = f'<img src="{img}" width="72" style="border-radius:50%;margin-bottom:.5rem">' if img else ""
    st.markdown(
        f'''<div class="pc-achievement">{img_html}
            <div style="font-family:var(--font-display);font-size:1.3rem;font-weight:700">🏆 {title}</div>
            <div style="color:var(--ink-2)">{subtitle}</div></div>''',
        unsafe_allow_html=True,
    )


def scientist_card(sci: dict, unlocked: bool) -> None:
    cls = "unlocked" if unlocked else "locked"
    st.markdown(
        f'''<div class="pc-card pc-sci {cls}" style="margin-bottom:.6rem">
              <img src="{sci['img']}">
              <div>
                <div style="font-family:var(--font-display);font-weight:600">{sci['nome']}
                  <span class="pc-badge amber" style="margin-left:.4rem">{sci['xp']} XP</span></div>
                <div style="font-size:.82rem;color:var(--ink-2)">{sci['bio']}</div>
                <div style="font-size:.82rem">{sci['contrib']}</div>
              </div>
            </div>''',
        unsafe_allow_html=True,
    )

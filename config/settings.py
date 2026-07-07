"""Configurações centrais do Physicscool."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = BASE_DIR / "questions"
STYLES_DIR = BASE_DIR / "styles"
LOCAL_DATA_DIR = BASE_DIR / ".local_data"

APP_NAME = "Physicscool"
APP_TAGLINE = "physics school · physics is cool"
SIMULADO_SIZE = 10          # mini simulado
SIMULADO_FULL_SIZE = 45     # simulado completo (formato prova real)
SIMULADO_FULL_TIMER = 5400  # 90 minutos
TIMER_OPTIONS = {"Sem tempo": 0, "5 min": 300, "10 min": 600, "15 min": 900,
                 "20 min": 1200, "30 min": 1800}
XP_PER_CORRECT = 15
XP_BONUS_STREAK = 5  # bônus por acerto em sequência dentro do simulado

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")

# Temas ↔ moeda de XP (ícone + nome + cor)
THEME_XP: dict[str, dict[str, str]] = {
    "Mecânica":      {"icon": "⚙️", "moeda": "Engrenagens", "color": "#94A3B8"},
    "Eletricidade":  {"icon": "⚡", "moeda": "Raios",       "color": "#FBBF24"},
    "Eletrostática": {"icon": "⚡", "moeda": "Raios",       "color": "#FBBF24"},
    "Magnetismo":    {"icon": "🧲", "moeda": "Ímãs",        "color": "#FB7185"},
    "Hidrostática":  {"icon": "💧", "moeda": "Gotas",       "color": "#38BDF8"},
    "Ondulatória":   {"icon": "🌊", "moeda": "Ondas",       "color": "#22D3EE"},
    "Termologia":    {"icon": "🔥", "moeda": "Chamas",      "color": "#FB923C"},
    "Óptica":        {"icon": "🔍", "moeda": "Lentes",      "color": "#A78BFA"},
    "Astronomia":    {"icon": "🌌", "moeda": "Estrelas",    "color": "#818CF8"},
}


def theme_meta(tema: str) -> dict[str, str]:
    """Metadados de gamificação de um tema (fallback neutro)."""
    return THEME_XP.get(tema, {"icon": "⚛️", "moeda": "Quanta", "color": "#22D3EE"})

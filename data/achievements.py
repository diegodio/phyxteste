"""=====================================================================
CATÁLOGO DE CONQUISTAS (medalhas)
=====================================================================
Cada conquista tem um `check(user, stats)` que devolve True quando
desbloqueada. Para criar uma nova, basta acrescentar um dicionário
nesta lista. `services/achievement_service.py` avalia todas.
=====================================================================
"""
from __future__ import annotations

ACHIEVEMENTS: list[dict] = [
    {"id": "primeira_questao", "nome": "Primeiro Contato", "icon": "👋",
     "desc": "Responda sua primeira questão.",
     "check": lambda u, s: u.questoes_respondidas >= 1},
    {"id": "q10", "nome": "Aquecendo", "icon": "🔥",
     "desc": "Responda 10 questões.",
     "check": lambda u, s: u.questoes_respondidas >= 10},
    {"id": "q100", "nome": "Centurião", "icon": "💯",
     "desc": "Responda 100 questões.",
     "check": lambda u, s: u.questoes_respondidas >= 100},
    {"id": "streak3", "nome": "Constância", "icon": "📅",
     "desc": "3 dias seguidos de estudo.",
     "check": lambda u, s: u.streak >= 3},
    {"id": "streak7", "nome": "Semana Perfeita", "icon": "🗓️",
     "desc": "7 dias seguidos de estudo.",
     "check": lambda u, s: u.streak >= 7},
    {"id": "xp500", "nome": "Meio Milhar", "icon": "✨",
     "desc": "Acumule 500 de XP total.",
     "check": lambda u, s: u.xp_total >= 500},
    {"id": "xp2000", "nome": "Mente Brilhante", "icon": "🌟",
     "desc": "Acumule 2000 de XP total.",
     "check": lambda u, s: u.xp_total >= 2000},
    {"id": "primeiro_simulado", "nome": "Na Arena", "icon": "⚡",
     "desc": "Complete seu primeiro simulado.",
     "check": lambda u, s: len(u.simulados) >= 1},
    {"id": "nota_maxima", "nome": "Gabaritou!", "icon": "🎯",
     "desc": "Acerte 100% em um simulado.",
     "check": lambda u, s: any(x["acertos"] == x["total"] and x["total"] > 0
                               for x in u.simulados)},
    {"id": "poliglota", "nome": "Físico Completo", "icon": "🧬",
     "desc": "Ganhe XP em 5 temas diferentes.",
     "check": lambda u, s: len(u.xp_por_tema) >= 5},
]

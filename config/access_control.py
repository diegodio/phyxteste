"""=====================================================================
CONTROLE DE ACESSO — edite APENAS este arquivo para gerenciar usuários.
=====================================================================

1) ALLOWED_EMAILS  → lista branca de e-mails que podem logar.
   Quem logar com e-mail fora da lista sofre LOGOUT AUTOMÁTICO.

2) PAGE_PERMISSIONS → quais páginas cada e-mail enxerga.
   Chaves de página disponíveis (usadas em app.py):
       home | questoes | simulado | resultado | trilhas
       perfil | estatisticas | materiais | praticar | revisar
       favoritas | conquistas | admin | professor | privacidade

   - Use "*" para liberar todas as páginas.
   - "_default" define a permissão de quem está na allowlist
     mas não tem entrada própria.

3) ALLOW_DEMO → True libera o botão "modo demonstração"
   (usuário demo recebe as permissões de "_demo").
"""
from __future__ import annotations

ALLOW_DEMO: bool = True

ALLOWED_EMAILS: list[str] = [
    "diego@exemplo.com",
    "paula@exemplo.com",
    "aluno1@exemplo.com",
]

PAGE_PERMISSIONS: dict[str, list[str]] = {
    # admin: tudo
    "diego@exemplo.com": ["*"],
    # exemplo: só estudo, sem estatísticas
    "aluno1@exemplo.com": ["home", "questoes", "simulado", "resultado",
                           "trilhas", "materiais", "praticar", "revisar",
                           "favoritas", "conquistas", "privacidade"],
    # permissão padrão p/ e-mails na allowlist sem entrada específica
    "_default": ["home", "questoes", "simulado", "resultado",
                 "trilhas", "perfil", "materiais", "praticar", "revisar",
                 "favoritas", "conquistas", "privacidade"],
    # permissão do usuário de demonstração
    "_demo": ["home", "questoes", "simulado", "resultado",
              "trilhas", "perfil", "estatisticas", "materiais",
              "praticar", "revisar", "favoritas", "conquistas", "privacidade"],
}


# ------------------------ API (não precisa editar) ------------------------
def is_email_allowed(email: str, demo: bool = False) -> bool:
    if demo:
        return ALLOW_DEMO
    return email.strip().lower() in {e.lower() for e in ALLOWED_EMAILS}


def pages_for(email: str, demo: bool = False) -> set[str]:
    """Conjunto de chaves de página permitidas para o usuário."""
    if demo:
        perms = PAGE_PERMISSIONS.get("_demo", [])
    else:
        perms = PAGE_PERMISSIONS.get(email.strip().lower(),
                                     PAGE_PERMISSIONS.get("_default", []))
    all_pages = {"home", "questoes", "simulado", "resultado", "trilhas",
                 "perfil", "estatisticas", "materiais", "praticar", "revisar",
                 "favoritas", "conquistas", "admin", "professor", "privacidade"}
    return all_pages if "*" in perms else set(perms) & all_pages

"""=====================================================================
TUTOR IA — explica erros usando modelos hospedados pela NVIDIA.
=====================================================================
Usa a NIM API (compatível com OpenAI: POST {base}/chat/completions).
Credenciais/modelo em config/ai_config.py (via .env).

Uso:
    tutor = AIService()
    if tutor.enabled:
        texto = tutor.explain_mistake(questao, alt_escolhida)
=====================================================================
"""
from __future__ import annotations

from typing import Optional

import requests

from config.ai_config import (AI_ENABLED, AI_MAX_TOKENS, AI_TEMPERATURE,
                              NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_MODEL)
from models.question import Question

_SYSTEM = (
    "Você é um tutor de Física paciente e didático para estudantes brasileiros "
    "de ensino médio que se preparam para o ENEM e vestibulares. Responda em "
    "português do Brasil, com no máximo 4 parágrafos curtos. Use LaTeX entre "
    "cifrões para fórmulas ($F = ma$). Nunca humilhe o aluno pelo erro."
)


class AIService:
    def __init__(self) -> None:
        self.enabled = AI_ENABLED

    # ------------------------- chamadas de alto nível -------------------------
    def explain_mistake(self, q: Question, escolhida: Optional[str]) -> str:
        """Explica por que a alternativa marcada está errada e a correta, certa."""
        alts = "\n".join(f"{a.id}) {a.texto}" for a in q.alternativas)
        marcada = escolhida or "(deixou em branco)"
        prompt = (
            f"O aluno errou esta questão de {q.tema} ({q.subtema}) do {q.prova} {q.ano}.\n\n"
            f"ENUNCIADO: {q.enunciado}\n\nALTERNATIVAS:\n{alts}\n\n"
            f"O aluno marcou: {marcada}. A correta é: {q.correct_id}.\n\n"
            "Explique: (1) qual foi provavelmente o raciocínio equivocado que levou "
            "à alternativa marcada; (2) o caminho correto de resolução, passo a passo; "
            "(3) uma dica curta para não repetir esse tipo de erro."
        )
        return self._chat(prompt)

    def study_tip(self, tema: str, taxa_acerto: float) -> str:
        """Dica de estudo personalizada para um tema fraco."""
        prompt = (
            f"Um aluno tem {taxa_acerto:.0f}% de acerto em {tema}. "
            "Dê um plano curto (3 passos) para melhorar nesse tema, citando "
            "os subtópicos mais cobrados no ENEM."
        )
        return self._chat(prompt)

    # ------------------------- chamada crua -------------------------
    def _chat(self, user_prompt: str) -> str:
        if not self.enabled:
            return ("🤖 Tutor IA desativado. Adicione `NVIDIA_API_KEY` no `.env` "
                    "(instruções em `config/ai_config.py`).")
        try:
            resp = requests.post(
                f"{NVIDIA_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {NVIDIA_API_KEY}",
                         "Content-Type": "application/json"},
                json={
                    "model": NVIDIA_MODEL,
                    "messages": [{"role": "system", "content": _SYSTEM},
                                 {"role": "user", "content": user_prompt}],
                    "max_tokens": AI_MAX_TOKENS,
                    "temperature": AI_TEMPERATURE,
                },
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except requests.RequestException as e:
            return f"🤖 Tutor indisponível no momento ({type(e).__name__}). Tente de novo."

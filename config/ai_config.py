"""=====================================================================
CONFIGURAÇÃO DE IA — modelos hospedados pela NVIDIA (NIM API)
=====================================================================
1. Crie uma conta em https://build.nvidia.com
2. Gere uma API key (começa com "nvapi-")
3. Coloque no .env:

     NVIDIA_API_KEY=nvapi-xxxxxxxxxxxx
     NVIDIA_MODEL=meta/llama-3.3-70b-instruct     # opcional
     NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1  # opcional

Sem a chave, o tutor fica desativado com aviso amigável (o resto do
site funciona normalmente). A API é compatível com o formato OpenAI
(/chat/completions), então trocar de modelo é só mudar NVIDIA_MODEL.
Modelos bons para tutoria em PT-BR: meta/llama-3.3-70b-instruct,
mistralai/mixtral-8x22b-instruct-v0.1, nvidia/llama-3.1-nemotron-70b-instruct.
=====================================================================
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_MODEL: str = os.getenv("NVIDIA_MODEL", "meta/llama-3.3-70b-instruct")
NVIDIA_BASE_URL: str = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

AI_ENABLED: bool = bool(NVIDIA_API_KEY)
AI_MAX_TOKENS: int = 700
AI_TEMPERATURE: float = 0.4

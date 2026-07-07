"""=====================================================================
TESTES AUTOMATIZADOS — núcleo do Physicscool.
=====================================================================
Rodar:  pytest tests/ -v
Cobre: SRS (SM-2), XP/níveis, metas, conquistas, filtros/busca,
modelo de questão, exportação PDF, controle de acesso e favoritos.
=====================================================================
"""
from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from config.access_control import is_email_allowed, pages_for
from models.question import Alternative, Question
from models.user import User
from services.achievement_service import AchievementService
from services.export_service import ExportService
from services.favorite_service import FavoriteService
from services.goal_service import GoalService
from services.srs_service import SRSService
from services.stats_service import StatsService
from services.xp_service import XPService


# ------------------------- fixtures -------------------------
@pytest.fixture
def user() -> User:
    return User(uid="test", nome="Aluno Teste", email="teste@exemplo.com")


@pytest.fixture
def question() -> Question:
    return Question(
        id="q1", prova="ENEM", ano=2024, tema="Mecânica", subtema="Cinemática",
        dificuldade="Fácil", enunciado="Qual a velocidade?",
        alternativas=[Alternative("A", "10", False), Alternative("B", "20", True),
                      Alternative("C", "30", False)])


# ------------------------- SRS -------------------------
class TestSRS:
    def test_erro_reinicia_para_amanha(self, user):
        SRSService.review(user, "q1", False)
        card = user.revisoes["q1"]
        assert card["intervalo"] == 1 and card["repeticoes"] == 0

    def test_acertos_crescem_intervalo(self, user):
        for _ in range(3):
            SRSService.review(user, "q1", True)
        assert user.revisoes["q1"]["intervalo"] > 3

    def test_facilidade_nunca_abaixo_do_minimo(self, user):
        for _ in range(20):
            SRSService.review(user, "q1", False)
        assert user.revisoes["q1"]["facilidade"] >= 1.3

    def test_due_detecta_vencidas(self, user):
        ontem = (date.today() - timedelta(days=1)).isoformat()
        amanha = (date.today() + timedelta(days=1)).isoformat()
        user.revisoes = {
            "vencida": {"intervalo": 1, "facilidade": 2.5, "repeticoes": 1,
                        "proxima": ontem, "ultima": ""},
            "futura": {"intervalo": 3, "facilidade": 2.5, "repeticoes": 1,
                       "proxima": amanha, "ultima": ""}}
        assert SRSService.due(user) == ["vencida"]
        assert SRSService.counts(user) == {"vencidas": 1, "agendadas": 1, "total": 2}


# ------------------------- XP e níveis -------------------------
class TestXP:
    def test_grant_soma_no_tema_e_no_total(self, user):
        XPService.grant(user, "Mecânica", 100)
        assert user.xp_por_tema["Mecânica"] == 100 and user.xp_total == 100

    def test_level_info_progressao(self):
        info0 = XPService.level_info("Eletricidade", 0)
        info_mid = XPService.level_info("Eletricidade", 200)
        assert info0["nivel"] == 0 and info_mid["nivel"] > 0
        assert 0 <= info_mid["progresso"] <= 1

    def test_trilha_completa(self):
        info = XPService.level_info("Eletricidade", 10**6)
        assert info["proximo"] is None and info["progresso"] == 1.0

    def test_tema_desconhecido_usa_default(self):
        assert XPService.level_info("Física Quântica", 50)["total_niveis"] > 0

    def test_bonus_streak(self):
        assert XPService.xp_for_answer(True, 1) < XPService.xp_for_answer(True, 3)
        assert XPService.xp_for_answer(False, 5) == 0


# ------------------------- metas -------------------------
class TestGoals:
    def test_registro_e_cumprimento(self, user):
        GoalService.register(user, 4)
        s = GoalService.status(user)
        assert s["feitas"] == 4 and not s["cumprida"]
        GoalService.register(user, 6)
        assert GoalService.status(user)["cumprida"]

    def test_meta_reinicia_em_novo_dia(self, user):
        user.meta_diaria = {"data": "2020-01-01", "meta": 10, "feitas": 8}
        assert GoalService.status(user)["feitas"] == 0


# ------------------------- conquistas -------------------------
class TestAchievements:
    def test_desbloqueio_unico(self, user):
        user.questoes_respondidas = 1
        novas = AchievementService.check_new(user)
        assert any(a["id"] == "primeira_questao" for a in novas)
        assert AchievementService.check_new(user) == []  # não repete

    def test_gabaritou(self, user):
        user.simulados = [{"acertos": 10, "total": 10, "respostas": [],
                           "data": "2024-01-01T00:00:00+00:00", "temas": [],
                           "tempo_gasto": 0, "xp_ganho": 0, "id": "x"}]
        assert any(a["id"] == "nota_maxima"
                   for a in AchievementService.check_new(user))


# ------------------------- questão -------------------------
class TestQuestion:
    def test_correct_id(self, question):
        assert question.correct_id == "B"

    def test_shuffle_deterministico_preserva_conteudo(self, question):
        s1 = question.shuffled(seed=7)
        s2 = question.shuffled(seed=7)
        assert [a.id for a in s1] == [a.id for a in s2]
        assert {a.id for a in s1} == {"A", "B", "C"}


# ------------------------- favoritos -------------------------
class TestFavorites:
    def test_toggle(self, user):
        assert FavoriteService.toggle(user, "q1") is True
        assert FavoriteService.is_fav(user, "q1")
        assert FavoriteService.toggle(user, "q1") is False


# ------------------------- export PDF -------------------------
class TestExport:
    def test_pdf_valido(self, user):
        pdf = ExportService.build_report(user, StatsService())
        assert pdf.startswith(b"%PDF-") and b"%%EOF" in pdf


# ------------------------- controle de acesso -------------------------
class TestAccess:
    def test_allowlist_case_insensitive(self):
        assert is_email_allowed("DIEGO@exemplo.com")
        assert not is_email_allowed("intruso@x.com")

    def test_demo_permitido(self):
        assert is_email_allowed("", demo=True)

    def test_admin_so_para_wildcard(self):
        assert "admin" in pages_for("diego@exemplo.com")
        assert "admin" not in pages_for("aluno1@exemplo.com")

    def test_default_sem_estatisticas(self):
        assert "estatisticas" not in pages_for("paula@exemplo.com")

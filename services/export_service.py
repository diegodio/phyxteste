"""=====================================================================
EXPORTAÇÃO DE RELATÓRIO EM PDF (histórico do aluno)
=====================================================================
Gera um PDF com resumo de desempenho usando apenas a biblioteca padrão
(sem dependências externas): monta um PDF mínimo válido em memória.
Para relatórios mais ricos, troque por reportlab/fpdf2 — a interface
`build_report(user, stats) -> bytes` permanece a mesma.
=====================================================================
"""
from __future__ import annotations

from datetime import datetime

from models.user import User


def _esc(t: str) -> str:
    return t.replace("(", r"\(").replace(")", r"\)").replace("\\", r"\\")


class ExportService:
    @staticmethod
    def build_report(user: User, stats) -> bytes:
        """Monta um PDF simples (uma página) com o resumo do aluno."""
        linhas = [
            "Physicscool - Relatorio de Desempenho",
            "",
            f"Aluno: {user.nome}",
            f"Email: {user.email or 'conta demo'}",
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "",
            f"XP total: {user.xp_total}",
            f"Questoes respondidas: {user.questoes_respondidas}",
            f"Simulados realizados: {len(user.simulados)}",
            f"Sequencia de estudo: {user.streak} dia(s)",
            f"Taxa de acerto: {stats.accuracy(user):.0f}%",
            "",
            "XP por tema:",
        ]
        for tema, xp in sorted(user.xp_por_tema.items(), key=lambda kv: -kv[1]):
            linhas.append(f"  - {tema}: {xp}")
        linhas += ["", "Conquistas desbloqueadas: " + str(len(user.conquistas))]

        return _simple_pdf(linhas)


def _simple_pdf(lines: list[str]) -> bytes:
    """PDF de uma página em texto (Helvetica 12) — sem libs externas."""
    y_start = 780
    content = ["BT", "/F1 14 Tf", f"1 0 0 1 60 {y_start} Tm", "16 TL"]
    for i, ln in enumerate(lines):
        size = 16 if i == 0 else 11
        content.append(f"/F1 {size} Tf")
        content.append(f"({_esc(ln)}) Tj")
        content.append("T*")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")

    objs = []
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objs.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream")

    pdf = b"%PDF-1.4\n"
    offsets = []
    for i, obj in enumerate(objs, start=1):
        offsets.append(len(pdf))
        pdf += b"%d 0 obj\n" % i + obj + b"\nendobj\n"
    xref_pos = len(pdf)
    pdf += b"xref\n0 %d\n" % (len(objs) + 1)
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += b"%010d 00000 n \n" % off
    pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\n" % (len(objs) + 1)
    pdf += b"startxref\n%d\n%%%%EOF" % xref_pos
    return pdf

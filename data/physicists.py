"""Trilhas de evolução por tema — cada nível é um cientista.

Cada entrada: nome, xp necessário, bio curta e contribuição para o tema.
`img` é um placeholder gerado por avatar (substituível por retratos reais).
"""
from __future__ import annotations


def _img(nome: str) -> str:
    return f"https://api.dicebear.com/9.x/notionists/svg?seed={nome.replace(' ', '')}"


def _sci(nome: str, xp: int, bio: str, contrib: str) -> dict:
    return {"nome": nome, "xp": xp, "bio": bio, "contrib": contrib, "img": _img(nome)}


TRACKS: dict[str, list[dict]] = {
    "Eletricidade": [
        _sci("Tales de Mileto", 30, "Filósofo grego (séc. VI a.C.).", "Observou a atração do âmbar atritado — a primeira nota sobre eletricidade."),
        _sci("William Gilbert", 80, "Médico inglês (1544–1603).", "Cunhou 'electricus' e distinguiu eletricidade de magnetismo."),
        _sci("Benjamin Franklin", 150, "Polímata americano (1706–1790).", "Cargas positiva/negativa e o experimento da pipa."),
        _sci("Charles Coulomb", 240, "Físico francês (1736–1806).", "Lei de Coulomb: a força entre cargas."),
        _sci("Alessandro Volta", 350, "Físico italiano (1745–1827).", "Inventou a pilha — a primeira corrente contínua."),
        _sci("André-Marie Ampère", 480, "Matemático francês (1775–1836).", "Fundou a eletrodinâmica; a unidade de corrente leva seu nome."),
        _sci("Georg Ohm", 640, "Físico alemão (1789–1854).", "Lei de Ohm: V = R·i."),
        _sci("Michael Faraday", 820, "Autodidata inglês (1791–1867).", "Indução eletromagnética e o conceito de campo."),
        _sci("James Clerk Maxwell", 1050, "Físico escocês (1831–1879).", "As quatro equações que unificaram eletricidade, magnetismo e luz."),
        _sci("Nikola Tesla", 1300, "Inventor sérvio-americano (1856–1943).", "Corrente alternada e motores de indução."),
    ],
    "Eletrostática": [
        _sci("Tales de Mileto", 30, "Filósofo grego.", "Primeiras observações de atração elétrica."),
        _sci("Charles du Fay", 90, "Químico francês (1698–1739).", "Dois tipos de eletricidade: vítrea e resinosa."),
        _sci("Benjamin Franklin", 180, "Polímata americano.", "Convenção de cargas + e −."),
        _sci("Charles Coulomb", 300, "Físico francês.", "Quantificou a força eletrostática."),
        _sci("Michael Faraday", 460, "Físico inglês.", "Gaiola de Faraday e linhas de campo."),
        _sci("Robert Millikan", 660, "Físico americano (1868–1953).", "Mediu a carga elementar do elétron."),
    ],
    "Mecânica": [
        _sci("Arquimedes", 30, "Matemático grego (287–212 a.C.).", "Alavancas e centro de gravidade."),
        _sci("Galileu Galilei", 90, "Físico italiano (1564–1642).", "Queda livre e inércia."),
        _sci("Johannes Kepler", 180, "Astrônomo alemão (1571–1630).", "As três leis do movimento planetário."),
        _sci("Isaac Newton", 300, "Físico inglês (1643–1727).", "As três leis do movimento e a gravitação universal."),
        _sci("Leonhard Euler", 460, "Matemático suíço (1707–1783).", "Mecânica do corpo rígido."),
        _sci("Joseph-Louis Lagrange", 660, "Matemático (1736–1813).", "Mecânica analítica."),
        _sci("William Hamilton", 900, "Matemático irlandês (1805–1865).", "Formulação hamiltoniana."),
        _sci("Emmy Noether", 1200, "Matemática alemã (1882–1935).", "Simetrias ↔ leis de conservação."),
    ],
    "Termologia": [
        _sci("Galileu Galilei", 30, "Físico italiano.", "Termoscópio, o ancestral do termômetro."),
        _sci("Anders Celsius", 90, "Astrônomo sueco (1701–1744).", "A escala centígrada."),
        _sci("James Joule", 180, "Físico inglês (1818–1889).", "Equivalente mecânico do calor."),
        _sci("Sadi Carnot", 300, "Engenheiro francês (1796–1832).", "O ciclo ideal das máquinas térmicas."),
        _sci("Rudolf Clausius", 460, "Físico alemão (1822–1888).", "Entropia e a 2ª lei."),
        _sci("Ludwig Boltzmann", 660, "Físico austríaco (1844–1906).", "Interpretação estatística da entropia."),
    ],
    "Ondulatória": [
        _sci("Pitágoras", 30, "Filósofo grego.", "Relações matemáticas dos sons musicais."),
        _sci("Christiaan Huygens", 90, "Físico holandês (1629–1695).", "Princípio de Huygens: luz como onda."),
        _sci("Thomas Young", 180, "Polímata inglês (1773–1829).", "Fenda dupla e interferência."),
        _sci("Christian Doppler", 300, "Físico austríaco (1803–1853).", "Efeito Doppler."),
        _sci("Heinrich Hertz", 460, "Físico alemão (1857–1894).", "Produziu e detectou ondas eletromagnéticas."),
    ],
    "Óptica": [
        _sci("Alhazen", 30, "Cientista árabe (965–1040).", "Fundou a óptica moderna com o 'Livro da Óptica'."),
        _sci("Willebrord Snell", 90, "Matemático holandês (1580–1626).", "Lei da refração."),
        _sci("Isaac Newton", 180, "Físico inglês.", "Decomposição da luz branca no prisma."),
        _sci("Augustin Fresnel", 300, "Físico francês (1788–1827).", "Difração e teoria ondulatória da luz."),
        _sci("Albert Einstein", 460, "Físico alemão (1879–1955).", "Efeito fotoelétrico: a luz também é partícula."),
    ],
    "Magnetismo": [
        _sci("Shen Kuo", 30, "Cientista chinês (1031–1095).", "Primeira descrição da bússola magnética."),
        _sci("William Gilbert", 90, "Médico inglês.", "A Terra é um grande ímã ('De Magnete')."),
        _sci("Hans Ørsted", 180, "Físico dinamarquês (1777–1851).", "Corrente elétrica gera campo magnético."),
        _sci("Michael Faraday", 300, "Físico inglês.", "Indução eletromagnética."),
        _sci("James Clerk Maxwell", 460, "Físico escocês.", "Unificação eletromagnética."),
    ],
    "Hidrostática": [
        _sci("Arquimedes", 30, "Matemático grego.", "Empuxo: o princípio de Arquimedes."),
        _sci("Simon Stevin", 90, "Engenheiro flamengo (1548–1620).", "Paradoxo hidrostático."),
        _sci("Evangelista Torricelli", 180, "Físico italiano (1608–1647).", "Barômetro e pressão atmosférica."),
        _sci("Blaise Pascal", 300, "Matemático francês (1623–1662).", "Princípio de Pascal — prensas hidráulicas."),
        _sci("Daniel Bernoulli", 460, "Matemático suíço (1700–1782).", "Equação de Bernoulli para fluidos."),
    ],
    "Astronomia": [
        _sci("Aristarco de Samos", 30, "Astrônomo grego.", "Primeiro modelo heliocêntrico."),
        _sci("Nicolau Copérnico", 90, "Astrônomo polonês (1473–1543).", "Revolução heliocêntrica."),
        _sci("Tycho Brahe", 180, "Astrônomo dinamarquês (1546–1601).", "Medições celestes de precisão inédita."),
        _sci("Johannes Kepler", 300, "Astrônomo alemão.", "Órbitas elípticas."),
        _sci("Edwin Hubble", 460, "Astrônomo americano (1889–1953).", "A expansão do universo."),
        _sci("Stephen Hawking", 660, "Físico inglês (1942–2018).", "Radiação de buracos negros."),
    ],
    "_default": [
        _sci("Aristóteles", 30, "Filósofo grego.", "Primeiras sistematizações da natureza."),
        _sci("Galileu Galilei", 120, "Físico italiano.", "O método experimental."),
        _sci("Isaac Newton", 300, "Físico inglês.", "A física clássica."),
        _sci("Albert Einstein", 600, "Físico alemão.", "Relatividade."),
    ],
}

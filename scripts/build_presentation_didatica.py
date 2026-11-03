"""14-slide didactic presentation: Monte Carlo for electronic instrumentation."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pptx import Presentation
import build_presentation as bp

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Apresentacao_MonteCarlo_Didatica.pptx"
FIG = ROOT / "slides" / "figures_didatica"


def add_body_with_image(prs, title, bullets, image, notes, *, size=22, img_frac=0.42):
    slide = bp.add_body_slide(prs, title, bullets, notes, size=size)
    body = bp.placeholder_by_idx(slide, 1)
    img_h = int(body.height * img_frac)
    img_top = body.top + body.height - img_h
    bp.add_picture_fit(slide, image, body.left, img_top, body.width, img_h)
    return slide


def build() -> Path:
    shutil.copyfile(bp.TEMPLATE, OUTPUT)
    prs = Presentation(str(OUTPUT))
    bp.delete_all_slides(prs)
    bp.rename_thanks_layout(prs)

    v5 = FIG / "01_indicacao_5V.png"
    pipe = FIG / "02_pipeline.png"
    gauss = FIG / "03_gaussiana.png"
    hist = FIG / "04_histograma_R.png"
    calib = FIG / "05_calibracao_MC.png"
    gif = FIG / "pi_quarto_circulo.gif"

    # 1
    bp.add_image_slide(
        prs,
        "Método de\nMonte Carlo",
        [
            "Jakson da Rocha Almeida",
            "Instrumentação Eletrônica",
            "PPEE / UFJF",
            "Se indica 5,00 V, a tensão é 5,00 V?",
        ],
        v5,
        "Abra com a pergunta. A indicação não é o valor verdadeiro: há incerteza de instrumento, "
        "calibração, resolução e ambiente. A questão da palestra: como obter a distribuição dos "
        "resultados possíveis quando várias fontes de incerteza atuam juntas.",
    )

    # 2
    add_body_with_image(
        prs,
        "O que é",
        [
            "Amostragem aleatória repetida",
            "para estimar o que o modelo produz",
        ],
        pipe,
        "Monte Carlo não é 'colocar ruído' no cálculo. As PDFs das entradas devem representar "
        "o conhecimento disponível sobre cada grandeza. Cinco etapas: entradas, sorteio, modelo, "
        "resultados, estatística.",
        size=24,
        img_frac=0.48,
    )

    # 3
    bp.add_body_slide(
        prs,
        "Contexto breve",
        [
            "Amostragem aleatória é anterior ao computador",
            "1940s: Ulam, von Neumann e o nome Monte Carlo",
            "Hoje: engenharia, risco e incerteza de medição",
        ],
        "O nome evoca os jogos de Mônaco. O método não nasceu na metrologia: foi incorporado "
        "porque propaga as incertezas das entradas até o resultado da medição. Um minuto neste slide.",
        size=22,
    )

    # 4
    bp.add_two_col_slide(
        prs,
        "Média e dispersão",
        [
            "Leituras V1, V2, …, VN",
            "Média = (soma das Vi) / N",
            "Valor típico das observações",
        ],
        [
            "Desvio-padrão s  (dispersão)",
            "Incerteza da média  ≈  s / √N",
            "Repetir não corrige viés sistemático",
        ],
        "Uma medição não é um número isolado. s descreve a dispersão das leituras; s/√N é a "
        "incerteza-padrão da média, se as condições estatísticas valem. Instrumento descalibrado "
        "não some ao repetir o ensaio.",
        size=18,
    )

    # 5
    bp.add_image_slide(
        prs,
        "Distribuições",
        [
            "Gaussiana: 68% · 95% · 99,7%",
            "são propriedades da normal,",
            "não regras universais.",
            "Resolução: muitas vezes uniforme.",
        ],
        gauss,
        "Se a entrada é modelada como normal, sorteamos dessa PDF. Nem toda grandeza é gaussiana: "
        "resolução de um DMM costuma ser retangular. Essa diversidade é uma vantagem do Monte Carlo.",
    )

    # 6
    bp.add_body_slide(
        prs,
        "O algoritmo",
        [
            "Y = f(X₁, X₂, …, Xₙ)",
            "Sortear as entradas  N  vezes",
            "Calcular cada Yₖ",
            "Média, s e intervalo de cobertura",
        ],
        "O laço é simples. O trabalho difícil é o modelo e as PDFs. Cada iteração é um cenário "
        "plausível. No fim, a amostra de Y é a distribuição empírica do mensurando.",
        size=22,
    )

    # 7  — quarter circle + GIF
    bp.add_image_slide(
        prs,
        "Estimando π",
        [
            "Quadrado [0, 1] × [0, 1]",
            "Quarto de círculo de raio 1",
            "vermelho:  x² + y² ≤ 1",
            "π̂  =  4 · r / n",
        ],
        gif,
        "Demonstração visual (GIF). Área do quadrado = 1; área do quarto de círculo = π/4. "
        "Por isso π̂ = 4 r/n, com r = pontos vermelhos. Com poucos pontos a estimativa oscila; "
        "o erro típico cai como 1/√N — para reduzir o erro à metade, cerca de 4 vezes mais pontos. "
        "No GIF, n = 5000, r = 3930 → π̂ ≈ 3,144.",
    )

    # 8
    bp.add_two_col_slide(
        prs,
        "Do π à engenharia",
        [
            "Estimativa de π",
            "coordenadas x, y",
            "teste x² + y² ≤ 1",
            "fração de pontos → π",
        ],
        [
            "Sistema de medição",
            "grandezas V, I, …",
            "modelo  Y = f(X)",
            "dispersão de Y → incerteza",
        ],
        "A analogia tem limite: no π, a aleatoriedade é do próprio sorteio geométrico. "
        "Em metrologia, as PDFs representam o conhecimento sobre as entradas; a simulação "
        "só propaga essa informação.",
        size=18,
    )

    # 9
    bp.add_body_slide(
        prs,
        "Na engenharia",
        [
            "Circuitos: tolerância de resistores",
            "Controle: incerteza de sensores",
            "Risco: probabilidade de violar um limite",
        ],
        "Sempre que há modelo matemático e incerteza nas entradas, Monte Carlo se aplica. "
        "Um minuto. Em seguida, o caso da disciplina: incerteza de medição.",
        size=22,
    )

    # 10
    bp.add_body_slide(
        prs,
        "Incerteza de medição",
        [
            "Y = f(X₁, …, Xₙ)    exemplo:  R = V / I",
            "GUM: derivadas e covariâncias",
            "Monte Carlo: propaga as PDFs",
            "u(y)  ≠  intervalo de cobertura",
        ],
        "Slide central. Incerteza-padrão é um desvio-padrão. Intervalo de cobertura (p.ex. 95%) "
        "não precisa ser simétrico nem igual a 2 u. Incluir correlação quando as entradas "
        "não são independentes.",
        size=20,
    )

    # 11
    bp.add_two_col_image_slide(
        prs,
        "Exemplo: R = V / I",
        [
            "V = 5,00 ± 0,05 V",
            "I = 0,100 ± 0,002 A",
            "R = 50,0 Ω",
            "GUM:  u(R) ≈ 1,12 Ω",
            "MCM:  desvio-padrão próximo",
        ],
        hist,
        "± interpretado como incerteza-padrão; entradas normais e independentes. "
        "80 mil ensaios: u(R) ≈ 1,12 Ω, alinhado ao GUM de primeira ordem. "
        "O histograma é a distribuição do resultado — mais informativo do que um único número.",
        size=18,
    )

    # 12
    bp.add_body_slide(
        prs,
        "Calibração",
        [
            "Modelo simples:  y = a x + b",
            "a e b também têm incerteza",
            "Sortear, recalcular, ver a saída",
            "Preservar correlação entre coeficientes",
        ],
        "Rotina de laboratório: relação indicação × referência. Coeficientes vêm dos dados e "
        "não são independentes. Sortear a e b à toa distorce a incerteza do valor corrigido. "
        "Útil em calibração não linear ou PDF assimétrica.",
        size=20,
    )

    # 13 — simulação real da calibração
    bp.add_two_col_image_slide(
        prs,
        "Calibração MC",
        [
            "Voltímetro:  y = a x + b",
            "10 pontos (1 a 10 V)",
            "30 000 ensaios",
            "corr(a, b) ≈ -0,89",
            "Em 5,00 V:",
            "V_corr = 4,975 V",
            "u ≈ 2,6 mV",
        ],
        calib,
        "Simulação feita de fato. Referência x de 1 a 10 V; indicação y = a x + b. "
        "Em cada ensaio, sorteiam-se incertezas da referência (2 mV) e da indicação (8 mV), "
        "refaz-se o ajuste linear e corrige-se y* = 5,00 V por x = (y* − b)/a. "
        "A nuvem (a, b) é alongada: correlação negativa típica da reta. "
        "Por isso não se pode sortear a e b independentemente. "
        "O histograma é a tensão corrigida; o desvio-padrão dessa amostra é u(V_corr).",
        size=16,
    )

    # 14
    bp.add_two_col_slide(
        prs,
        "Vantagens e limites",
        [
            "Modelos não lineares",
            "Várias PDFs",
            "Distribuição completa de Y",
            "Intervalos de cobertura",
        ],
        [
            "Custa mais CPU que o GUM",
            "Modelo ruim → resultado ruim",
            "Não corrige viés desconhecido",
            "Eventos raros exigem N grande",
        ],
        "Frase de fechamento deste bloco: a qualidade do Monte Carlo é a qualidade do modelo, "
        "das PDFs e do número de ensaios — não só do N.",
        size=18,
    )

    # 15
    bp.add_two_col_slide(
        prs,
        "Conclusão",
        [
            "A indicação não é o valor sem incerteza",
            "Modelo → PDFs → distribuição de Y",
            "Ferramenta para medição e calibração",
        ],
        [
            "JCGM 100:2008  (GUM)",
            "JCGM 101:2008  (Monte Carlo)",
            "bipm.org  ·  JCGM publications",
        ],
        "Retome o 5,00 V. Monte Carlo não substitui o GUM: complementa, sobretudo quando o "
        "modelo é não linear ou a PDF de saída não é gaussiana. Abrir para perguntas.",
        size=16,
    )

    prs.save(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    path = build()
    prs = Presentation(str(path))
    print(f"saved {path}")
    print(f"slides {len(prs.slides)}")
    for i, s in enumerate(prs.slides, 1):
        title = s.shapes.title.text.replace("\n", " ") if s.shapes.title else ""
        print(f"{i:02d}  {s.slide_layout.name:32}  {title}")

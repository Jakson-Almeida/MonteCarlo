"""Build the 23-slide Monte Carlo / metrology presentation from Template.pptx."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "Template.pptx"
OUTPUT = ROOT / "Apresentacao_MonteCarlo_Metrologia.pptx"
FIGURES = ROOT / "slides" / "figures"

LAYOUT_SECTION_IMAGE = 0  # title + subtitle left, image right
LAYOUT_TITLE = 1
LAYOUT_TITLE_BODY = 2
LAYOUT_TWO_COL = 3
LAYOUT_THANKS = 4

BROWN = RGBColor(0x69, 0x5D, 0x46)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x3D, 0x35, 0x28)


def delete_all_slides(prs: Presentation) -> None:
    sld_id_lst = prs.slides._sldIdLst
    for sld_id in list(sld_id_lst):
        r_id = sld_id.get(qn("r:id"))
        prs.part.drop_rel(r_id)
        sld_id_lst.remove(sld_id)


def placeholder_by_idx(slide, idx: int):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    raise KeyError(f"placeholder idx {idx} not found")


def set_run_font(run, *, size=None, bold=None, color=None, name="Arial"):
    run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def set_placeholder_text(ph, text: str, *, size=None, bold=None, color=None, align=None):
    tf = ph.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    if align is not None:
        p.alignment = align
    run = p.add_run()
    run.text = text
    set_run_font(run, size=size, bold=bold, color=color)
    return tf


def set_multiline(ph, lines: list[str], *, size=20, bold=False, color=None, align=None, space_after=8):
    tf = ph.text_frame
    tf.clear()
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(space_after)
        if align is not None:
            p.alignment = align
        run = p.add_run()
        run.text = line
        set_run_font(run, size=size, bold=bold, color=color)
    return tf


def set_notes(slide, text: str) -> None:
    notes = slide.notes_slide
    notes.notes_text_frame.text = text


def add_picture_fit(slide, path: Path, left, top, width, height) -> None:
    im = Image.open(path)
    ar = im.width / im.height
    box_ar = width / height
    if ar > box_ar:
        h = int(width / ar)
        t = top + (height - h) // 2
        slide.shapes.add_picture(str(path), left, t, width=width, height=h)
    else:
        w = int(height * ar)
        l = left + (width - w) // 2
        slide.shapes.add_picture(str(path), l, top, width=w, height=height)


def hide_placeholder(ph) -> None:
    """Keep layout but make leftover prompt text invisible."""
    tf = ph.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = ""
    spPr = ph._element.spPr
    solid = spPr.makeelement(qn("a:solidFill"), {})
    srgb = solid.makeelement(qn("a:srgbClr"), {"val": "FFFFFF"})
    alpha = srgb.makeelement(qn("a:alpha"), {"val": "0"})
    srgb.append(alpha)
    solid.append(srgb)
    # do not force fill; just empty text


def add_title_slide(prs, title: str, subtitle: str, notes: str):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE])
    set_placeholder_text(
        placeholder_by_idx(slide, 0),
        title,
        size=32,
        bold=True,
        color=DARK,
        align=PP_ALIGN.CENTER,
    )
    set_placeholder_text(
        placeholder_by_idx(slide, 1),
        subtitle,
        size=16,
        color=BROWN,
        align=PP_ALIGN.CENTER,
    )
    set_notes(slide, notes)
    return slide


def add_body_slide(prs, title: str, bullets: list[str], notes: str, *, size=24):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE_BODY])
    set_placeholder_text(placeholder_by_idx(slide, 0), title, size=22, bold=True, color=WHITE)
    set_multiline(placeholder_by_idx(slide, 1), bullets, size=size, color=DARK, space_after=16)
    set_notes(slide, notes)
    return slide


def add_two_col_slide(prs, title: str, left: list[str], right: list[str], notes: str, *, size=20):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TWO_COL])
    set_placeholder_text(placeholder_by_idx(slide, 0), title, size=26, bold=True, color=DARK)
    set_multiline(placeholder_by_idx(slide, 1), left, size=size, color=DARK, space_after=12)
    set_multiline(placeholder_by_idx(slide, 2), right, size=size, color=DARK, space_after=12)
    set_notes(slide, notes)
    return slide


def add_image_slide(prs, title: str, subtitle_lines: list[str], image: Path, notes: str):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_SECTION_IMAGE])
    set_placeholder_text(placeholder_by_idx(slide, 0), title, size=26, bold=True, color=DARK)
    set_multiline(
        placeholder_by_idx(slide, 1),
        subtitle_lines,
        size=16,
        color=BROWN,
        space_after=8,
    )
    img_ph = placeholder_by_idx(slide, 2)
    hide_placeholder(img_ph)
    add_picture_fit(slide, image, img_ph.left, img_ph.top, img_ph.width, img_ph.height)
    set_notes(slide, notes)
    return slide


def add_two_col_image_slide(prs, title: str, left: list[str], image: Path, notes: str, *, size=18):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TWO_COL])
    set_placeholder_text(placeholder_by_idx(slide, 0), title, size=26, bold=True, color=DARK)
    set_multiline(placeholder_by_idx(slide, 1), left, size=size, color=DARK, space_after=12)
    right = placeholder_by_idx(slide, 2)
    hide_placeholder(right)
    add_picture_fit(slide, image, right.left, right.top, right.width, right.height)
    set_notes(slide, notes)
    return slide


def rename_thanks_layout(prs: Presentation) -> None:
    layout = prs.slide_layouts[LAYOUT_THANKS]
    for shape in layout.shapes:
        if shape.has_text_frame and "Acknowledgement" in shape.text:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if "Acknowledgement" in run.text:
                        run.text = run.text.replace("Acknowledgement", "Obrigado")


def add_thanks_slide(prs, notes: str):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_THANKS])
    set_notes(slide, notes)
    return slide


def build() -> Path:
    shutil.copyfile(TEMPLATE, OUTPUT)
    prs = Presentation(str(OUTPUT))
    delete_all_slides(prs)
    rename_thanks_layout(prs)

    fig2 = FIGURES / "01_jcgm_fig2_propagacao.png"
    fig4 = FIGURES / "02_jcgm_fig4_etapas_mcm.png"
    fig9 = FIGURES / "03_jcgm_fig9_gum_vs_mcm.png"
    osc = FIGURES / "04_imeko_fig2_bancada_osciloscopio.png"
    pdf_lab = FIGURES / "05_imeko_fig6_pdf_montecalc.png"
    conf = FIGURES / "06_imeko_fig7_conformidade.png"
    vna = FIGURES / "07_mms_fig5_diagrama_vna.png"
    corr = FIGURES / "08_mms_fig7_mcm_vs_gum.png"

    # 1
    add_title_slide(
        prs,
        "Monte Carlo na metrologia",
        "Jakson da Rocha Almeida\nInstrumentação Eletrônica · PPEE · UFJF",
        "Apresentação da disciplina de Instrumentação Eletrônica. "
        "Foco: o que é Monte Carlo, o uso em metrologia (JCGM 101) e duas aplicações de laboratório.",
    )

    # 2
    add_body_slide(
        prs,
        "Roteiro",
        [
            "O que é Monte Carlo",
            "O contexto na metrologia",
            "Duas bancadas de instrumentação",
        ],
        "Três blocos. Primeiro a ideia do método, depois o GUM e o JCGM 101, "
        "e por fim osciloscópio e sensor de RF com VNA.",
    )

    # 3
    add_title_slide(
        prs,
        "Como avaliar a incerteza\nquando o modelo não é linear?",
        "A pergunta que o laboratório precisa responder",
        "O GUM clássico lineariza o modelo. Em muitos instrumentos isso não basta. "
        "Monte Carlo entra exatamente nesse ponto.",
    )

    # 4
    add_body_slide(
        prs,
        "A ideia",
        [
            "Sortear as entradas do modelo",
            "Recalcular a saída muitas vezes",
            "Ler a distribuição do resultado",
        ],
        "Não se simula um processo físico aleatório: amostram-se as PDFs das grandezas de entrada "
        "e propaga-se cada amostra pelo modelo de medição Y = f(X).",
    )

    # 5
    add_image_slide(
        prs,
        "Propagação de\ndistribuições",
        [
            "Y = f(X₁, …, Xₙ)",
            "As PDFs de entrada geram a PDF de Y.",
        ],
        fig2,
        "Figura 2 do JCGM 101: três entradas com PDFs diferentes passam pelo modelo. "
        "A saída pode ser assimétrica mesmo se algumas entradas forem gaussianas.",
    )

    # 6
    add_body_slide(
        prs,
        "O método entrega",
        [
            "Estimativa do mensurando",
            "Incerteza-padrão u(y)",
            "Intervalo de abrangência",
        ],
        "Com a amostra de Y: média como estimativa, desvio-padrão como u(y), "
        "e percentis para o intervalo de abrangência (em geral 95%).",
    )

    # 7
    add_title_slide(
        prs,
        "Contexto em metrologia",
        "Do GUM clássico ao JCGM 101",
        "Seção de enquadramento normativo. O GUM continua válido; o Monte Carlo é o suplemento "
        "quando as hipóteses do GUM não se sustentam.",
    )

    # 8
    add_body_slide(
        prs,
        "GUM clássico",
        [
            "Lei de propagação de incertezas",
            "Aproximação gaussiana da saída",
            "U = k · u(y)",
        ],
        "O GUM usa derivadas (coeficientes de sensibilidade) e assume, na prática, "
        "saída gaussiana ou t de Student. O intervalo expandido é k vezes a incerteza-padrão.",
    )

    # 9
    add_two_col_slide(
        prs,
        "Quando o GUM falha",
        [
            "Modelo não linear",
            "Linearização ruim",
            "Derivadas incompletas",
        ],
        [
            "PDF assimétrica",
            "± k·u engana a cobertura",
            "Intervalo deslocado",
        ],
        "Dois gatilhos do JCGM 101: o modelo não admite boa linearização, "
        "ou a PDF de Y se afasta claramente de uma gaussiana.",
    )

    # 10
    add_image_slide(
        prs,
        "JCGM 101",
        [
            "Suplemento 1 do GUM (2008)",
            "Monte Carlo para incerteza de medição",
        ],
        fig4,
        "Fluxograma oficial: PDFs de entrada, modelo, M ensaios, representação discreta de Y, "
        "estimativa, u(y) e intervalo [y_low, y_high].",
    )

    # 11
    add_body_slide(
        prs,
        "Quatro passos",
        [
            "Amostrar as PDFs de entrada",
            "Avaliar o modelo",
            "Resumir a amostra de Y",
            "Obter o intervalo de abrangência",
        ],
        "Versão falada do fluxograma. M típico: 10⁵ a 10⁶ ensaios. "
        "O intervalo pode ser simétrico em probabilidade ou o de menor comprimento.",
    )

    # 12
    add_two_col_image_slide(
        prs,
        "GUM vs Monte Carlo",
        [
            "Vermelho: GUM (gaussiana)",
            "Azul: histograma MCM",
            "Linhas: intervalos de 95%",
            "A cobertura não coincide",
        ],
        fig9,
        "Figura 9 do JCGM 101. Uma entrada dominante e larga deixa Y longe da gaussiana. "
        "O intervalo do GUM (tracejado) fica diferente do intervalo do Monte Carlo (sólido).",
    )

    # 13
    add_title_slide(
        prs,
        "Aplicação em instrumentação",
        "Osciloscópio · Sensor de RF com VNA",
        "Dois laboratórios reais. Mesma pergunta: GUM basta, ou o Monte Carlo muda a incerteza "
        "e a decisão de conformidade?",
    )

    # 14
    add_image_slide(
        prs,
        "Calibração de\nosciloscópio",
        [
            "Alta frequência, rastreável ao SI",
            "Calibrador + osciloscópio 3 GHz",
        ],
        osc,
        "Cundeva-Blajer et al., Acta IMEKO 2026. Bancada alinhada à EURAMET cg-7. "
        "O UUT1 é um osciloscópio de 3 GHz, 4 canais.",
    )

    # 15
    add_image_slide(
        prs,
        "PDF no laboratório",
        [
            "MonteCalc em LabVIEW",
            "Distribuição no ponto 2 V/div",
        ],
        pdf_lab,
        "A ferramenta gera a PDF da tensão no ponto de calibração. "
        "No paper, a incerteza expandida por Monte Carlo chegou a 2,5 vezes a do GUM nesse ponto.",
    )

    # 16
    add_image_slide(
        prs,
        "Conformidade",
        [
            "Regras ILAC G8",
            "A incerteza entra na decisão de aceite",
        ],
        conf,
        "Gráfico de conformidade: medido, incerteza e limites. "
        "Mudar de GUM para Monte Carlo pode mudar a faixa de guarda e o parecer.",
    )

    # 17
    add_image_slide(
        prs,
        "Sensor de potência RF",
        [
            "Calibração com VNA",
            "Gerador, acopladores e sensores",
        ],
        vna,
        "Jaworski et al., Metrology and Measurement Systems 2023. "
        "Sistema de comparação direta com VNA Keysight N5225B para o fator de calibração.",
    )

    # 18
    add_two_col_image_slide(
        prs,
        "A lição da correlação",
        [
            "Sem covariância, o MCM dispara",
            "Medidas juntas não são independentes",
            "Com a matriz, GUM e MCM convergem",
        ],
        corr,
        "Figura 7 do paper de RF: diferença relativa MCM−GUM de centenas de por cento no fator de calibração "
        "quando a correlação é ignorada. Com a matriz de covariância, os métodos se aproximam.",
        size=18,
    )

    # 19
    add_two_col_slide(
        prs,
        "As duas bancadas",
        [
            "Osciloscópio",
            "PDF da tensão",
            "Decisão de conformidade",
        ],
        [
            "VNA + sensor de RF",
            "Fator de calibração",
            "Correlação entre entradas",
        ],
        "Uma bancada mostra o efeito da forma da PDF e da conformidade. "
        "A outra mostra que tratar entradas correlacionadas como independentes invalida o Monte Carlo.",
    )

    # 20
    add_body_slide(
        prs,
        "Para o laboratório",
        [
            "O modelo do instrumento importa",
            "A forma da PDF importa",
            "Correlação não pode ser ignorada",
        ],
        "Três mensagens para levar: escrever bem Y = f(X), não assumir gaussiana sem olhar a amostra, "
        "e incluir covariância quando as grandezas são medidas juntas.",
    )

    # 21
    add_body_slide(
        prs,
        "Cuidado prático",
        [
            "Número suficiente de ensaios",
            "Modelo fiel à medição",
            "MCM não corrige modelo errado",
        ],
        "M pequeno deixa o intervalo instável. Modelo incompleto propaga o erro. "
        "Monte Carlo é numérico: a qualidade do resultado é a qualidade do modelo e das PDFs.",
    )

    # 22
    add_body_slide(
        prs,
        "Referências",
        [
            "JCGM 101:2008 — GUM Supplement 1",
            "Cundeva-Blajer et al., Acta IMEKO, 2026",
            "Jaworski et al., Metrol. Meas. Syst., 2023",
        ],
        "Documentos de acesso aberto usados nesta apresentação. "
        "Há também a tradução do INMETRO do JCGM 101 e o extra da PTB sobre experimentos virtuais.",
        size=18,
    )

    # 23
    add_thanks_slide(
        prs,
        "Encerramento. Abrir para perguntas sobre o algoritmo, as bancadas ou a comparação GUM versus Monte Carlo.",
    )

    prs.save(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    path = build()
    prs = Presentation(str(path))
    print(f"saved {path}")
    print(f"slides {len(prs.slides)}")
    for i, s in enumerate(prs.slides, 1):
        title = ""
        if s.shapes.title:
            title = s.shapes.title.text.replace("\n", " ")
        print(f"{i:02d}  {s.slide_layout.name:32}  {title}")

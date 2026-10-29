# Monte Carlo na metrologia

Material inicial para a disciplina de **Instrumentação Eletrônica**, Programa de Pós-Graduação em Engenharia Elétrica (PPEE), UFJF.

Os PDFs estão em [`papers/`](papers/). Todos são de acesso aberto (BIPM, INMETRO, Acta IMEKO, PAN Journals, arXiv).

## Os 3 papers principais

### 1. Documento normativo — GUM Supplement 1 (JCGM 101:2008)

O texto de referência internacional para avaliar incerteza de medição por **propagação de distribuições com Monte Carlo**, como alternativa ao GUM clássico (lei de propagação de incertezas + aproximação gaussiana).

- **JCGM.** *Evaluation of measurement data — Supplement 1 to the “Guide to the expression of uncertainty in measurement” — Propagation of distributions using a Monte Carlo method.* JCGM 101:2008. BIPM, 2008.
- Arquivo (inglês, 90 p.): [`papers/01_JCGM_101_2008_GUM_Supplement1_MonteCarlo.pdf`](papers/01_JCGM_101_2008_GUM_Supplement1_MonteCarlo.pdf)
- Arquivo (tradução autorizada INMETRO, 130 p.): [`papers/01b_INMETRO_JCGM_101_2008_PT_MonteCarlo.pdf`](papers/01b_INMETRO_JCGM_101_2008_PT_MonteCarlo.pdf)
- Fonte: [BIPM](https://www.bipm.org/documents/20126/2071204/JCGM_101_2008_E.pdf) · [INMETRO](https://www.gov.br/inmetro/pt-br/centrais-de-conteudo/publicacoes/suplemento-montecarlo.pdf)

**Por que entra na disciplina.** Define quando o GUM linearizado falha (modelo não linear, PDF de saída assimétrica) e descreve o algoritmo: amostrar as PDFs das grandezas de entrada, avaliar o modelo de medição, obter média, incerteza-padrão e intervalo de abrangência.

### 2. Aplicação em instrumentação elétrica — calibração de osciloscópio

Compara GUM e Monte Carlo na calibração rastreável de instrumentos de alta frequência (osciloscópio > 500 MHz), com software em LabVIEW e avaliação de conformidade (ILAC G8).

- **Cundeva-Blajer, M.; Dimitrovski, G.; Nakova, M.; Demerdziev, K.** Monte Carlo-based uncertainty quantification for conformity assessment and traceable calibration of high-frequency instrumentation. *Acta IMEKO*, v. 15, n. 2, p. 1–20, 2026. DOI: [10.21014/actaimeko.v15i2.2285](https://doi.org/10.21014/actaimeko.v15i2.2285)
- Arquivo (20 p.): [`papers/02_Cundeva-Blajer_2026_MonteCarlo_HF_instrumentation.pdf`](papers/02_Cundeva-Blajer_2026_MonteCarlo_HF_instrumentation.pdf)
- Fonte: [Acta IMEKO (PDF)](https://acta.imeko.org/index.php/acta-imeko/article/download/2285/3213)

**Por que entra na disciplina.** É o paper mais próximo de Instrumentação Eletrônica: osciloscópio, rastreabilidade SI, orçamento de incerteza e decisão de conformidade.

### 3. Aplicação em RF — sensor de potência + VNA

Aplica Monte Carlo à incerteza Tipo A na calibração de sensor de potência de RF com analisador de redes vetorial (VNA). Mostra o efeito de correlação (matriz de covariância) e da forma da PDF sobre o intervalo de incerteza.

- **Jaworski, M.; Szatkowski, J.; Kossek, T.** Determination of measurement uncertainty by a Monte Carlo method for an RF power sensor calibration system using a VNA. *Metrology and Measurement Systems*, v. 30, n. 4, p. 703–720, 2023. DOI: [10.24425/mms.2023.147953](https://doi.org/10.24425/mms.2023.147953)
- Arquivo (18 p.): [`papers/03_RF_power_sensor_MonteCarlo_VNA_MMS_2023.pdf`](papers/03_RF_power_sensor_MonteCarlo_VNA_MMS_2023.pdf)
- Fonte: [PAN Journals (PDF)](https://journals.pan.pl/Content/130309/art07_int.pdf?handler=pdf)

**Por que entra na disciplina.** Liga Monte Carlo a um arranjo clássico de laboratório de RF (VNA, conectores, fator de calibração) e ilustra um erro comum: ignorar correlação entre grandezas de entrada.

## Extra (opcional)

- **Hughes, F.; Marschall, M.; Wübbeler, G.; Kok, G.; van Dijk, M.; Elster, C.** JCGM 101-compliant uncertainty evaluation using virtual experiments. XXIV IMEKO World Congress, Hamburgo, 2024. [arXiv:2404.10530](https://arxiv.org/abs/2404.10530)
- Arquivo: [`papers/extra_Hughes_2024_JCGM101_virtual_experiments.pdf`](papers/extra_Hughes_2024_JCGM101_virtual_experiments.pdf)

Estende o JCGM 101 a experimentos virtuais e modelos não lineares (PTB / VSL). Útil se o trabalho seguir para simulação numérica do instrumento.

## Leitura sugerida

1. JCGM 101 (versão PT do INMETRO): introdução, cláusulas do método Monte Carlo e exemplos.
2. Cundeva-Blajer et al. (2026): ver como o método vira procedimento de calibração de osciloscópio.
3. Jaworski et al. (2023): prestar atenção em PDF, covariância e comparação GUM vs MCM.

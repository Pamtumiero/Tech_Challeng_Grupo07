# 📊 Olist — Tech Challenge Fase 1 (POSTECH DTAT)

Análise do **Brazilian E-Commerce Public Dataset by Olist** (Kaggle).
**Problema central do challenge:**
**Atrair mais investidores**

**Foco do grupo para atacar a proposta:**
**Geografia e Categorias** — A problemática na distribuição e venda no território brasileiro.

> **Alunos:** 
> 1. Lucas Aguiar de Moura - rm375551
> 2. ⁠Pamela Regina Tumiero da Costa - rm374909
> 3. ⁠Guilherme Augusto Justino da Silva - rm374370
> 4. ⁠Mariana Nogueira Salgado Zeron - rm374774
> 5. Vitor Martino - rm374436
> 
> **Curso:** POSTECH DTAT — Tech Challenge Fase 1
> 
> **Foco da apresentação:** Geografia e Categorias (Nordeste e Centro-Oeste). Os demais estudos (crescimento,
> top performers, profundidade/RFM) entram como **análises de apoio**.

---

## 🚀 TL;DR — a tese geográfica
| | |
|---|---|
| 📍 **64,6%** da receita no Sudeste | a Olist é, na prática, um e-commerce do Sudeste |
| 🏪 NE **56** e CO **79** sellers locais (Sul = 668) | **falta oferta local**, não demanda |
| 🚚 Frete **~31% do preço no NE** · ticket mais alto do país | frete **filtra** a compra pequena |
| ⏱️ Entrega: transporte 6d (SE) → **14d (NE)** · nota NE **3,97** | gargalo é o **transporte**, não o seller |

**Causa raiz única:** a **oferta está longe do cliente**. NE/CO compram pouco **e** recebem atrasado pelo mesmo
motivo. A prova: onde o vendedor é do **mesmo estado**, o NE entrega em 7 dias (= Sudeste). **Recomendação central:**
aproximar a oferta — **fulfillment distribuído nos estados-âncora (BA, PE, CE)**, não um hub único — + recrutar
sellers locais, medindo pela **satisfação** das regiões (NE 3,97 → 4,15).

---

## 🗂️ Estrutura do repositório
```
tech_challenge_olist/
├── data/                       # 9 CSVs do Olist (NÃO versionados — baixar do Kaggle)
├── notebooks/
│   ├── 02_geografia_categorias.ipynb     # ★ ANÁLISE CENTRAL (Q1 + Q2 + categorias + satisfação)
│   ├── 01_crescimento_receita.ipynb      # apoio: crescimento e receita
│   ├── 03_top_performers.ipynb           # apoio: top performers
│   └── 04_profundidade_rfm.ipynb         # apoio: profundidade (logística, satisfação, RFM)
├── figs/                       # 22 gráficos gerados (p1_…p4_)
├── outputs/                    # CSVs de KPIs e tabelas auxiliares
├── docs/
│   ├── data_dictionary.md
│   ├── documentacao_tecnica.md
│   └── recomendacoes_consolidadas.md     # consolidação executiva
├── apresentacao/
│   ├── Relatorio_Tech_Challenge_Olist_ABNT_FIAP.docx    # documento final para entrega do trabalho em docx
│   ├── Relatorio_Tech_Challenge_Olist_ABNT_FIAP.pdf     # documento final para entrega do trabalho em pdf
│   └── apresentacao_executiva.pptx                      # deck executivo
├── requirements.txt
└── README.md
```

## ⚙️ Como rodar
```bash
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt
# baixar os 9 CSVs do Kaggle para data/
jupyter lab    # abrir notebooks/ e "Run All"
```

## 🧭 Estrutura analítica
| Papel | Tema | Entrega |
|---|---|---|
| ★ **Central** | **Geografia e categorias** | Q1 (oferta/frete/ticket), Q2 (gargalo de entrega), categorias×região, satisfação, recomendações com metas |
| apoio | Crescimento e receita | evolução mensal, YoY, sazonalidade, volume×preço |
| apoio | Top performers | ranking produtos/sellers, Pareto, priorização |
| apoio | Profundidade | logística, satisfação, RFM, churn, cross-sell |
| — | Apresentação | relatório HTML, deck e vídeo executivo — **focados no problema geográfico** |

## 📚 Fonte dos dados
[Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
Dados não versionados neste repositório (licença/volume) — baixe e coloque em `data/`.

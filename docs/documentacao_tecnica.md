# 🛠️ Documentação Técnica — Tech Challenge Fase 1 (Olist)

## 1. Visão geral
Projeto de análise do *Brazilian E-Commerce Public Dataset by Olist* para o Tech Challenge Fase 1
(POSTECH DTAT). A entrega é dividida em **5 frentes** (uma por pessoa da equipe), cada uma com notebook
reprodutível, gráficos e recomendações acionáveis, consolidadas em uma narrativa executiva de investimento.

| Frente | Notebook | Trilha |
|---|---|---|
| Crescimento e Receita | `notebooks/01_crescimento_receita.ipynb` | 1 |
| Geografia e Categorias | `notebooks/02_geografia_categorias.ipynb` | 1 / 5 |
| Top Performers | `notebooks/03_top_performers.ipynb` | 1 / 5 |
| Profundidade (logística, satisfação, RFM, cross-sell) | `notebooks/04_profundidade_rfm.ipynb` | 3 / 4 / 5 |
| Storytelling executivo, apresentação e vídeo | `apresentacao/` | — |

## 2. Stack
- **Python 3.12**, **pandas 2.2**, numpy, matplotlib, seaborn
- Notebooks Jupyter executados de ponta a ponta (saídas embutidas) via `nbconvert`
- Sem dependência de internet; tudo roda offline sobre os CSVs em `data/`

> Nota pandas ≥ 2.2: `'M'` foi depreciado como frequência de resample — usar `'ME'`/`'MS'`.

## 3. Como reproduzir
```bash
# 1. criar ambiente
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. colocar os 9 CSVs do Olist em data/  (baixar do Kaggle)

# 3a. rodar os notebooks no Jupyter
jupyter lab    # abrir notebooks/ e Run All

# 3b. OU regenerar tudo via scripts (gera figs/ + outputs/ e re-executa os .ipynb)
cd src
python gen_pessoa1.py
python gen_pessoa2.py
python gen_pessoa3.py
python gen_pessoa4.py
```

## 4. Arquitetura do código
- **`src/build_common.py`** — fábrica de notebooks. Centraliza:
  - bloco de **setup** padrão (imports, tema visual, paleta);
  - bloco de **carga** dos 9 datasets;
  - bloco de **escopo canônico** (`orders_v`, `items_full`, receita por pedido, lead time);
  - helpers `md()` / `code()` e `write_and_run()` (monta o `.ipynb` e executa com `ExecutePreprocessor`).
- **`src/gen_pessoaN.py`** — cada gerador monta o notebook da sua frente reusando `build_common`.
  Garante que **todas as frentes partem exatamente do mesmo escopo de dados** (consistência de números).

Essa separação evita divergência de KPIs entre notebooks (o problema clássico de "cada um filtrou diferente")
e torna a regeneração determinística.

## 5. Definições de métricas (contrato analítico)
| Métrica | Fórmula | Observação |
|---|---|---|
| Escopo do pedido | `order_status == "delivered"` (apenas entregues) | não entregues mostrados no adendo e excluídos |
| Receita / faturamento | `Σ(price) + Σ(freight_value)` por `order_id` | visão GMV (inclui frete) |
| **Ticket médio** | `Σ(price) / nº de pedidos` | **só mercadoria — NÃO inclui frete** |
| Cliente único | distinct `customer_unique_id` | nunca `customer_id` |
| Lead time | `delivered_customer_date − purchase_timestamp` (dias) | nulos descartados |
| No prazo | `delivered_customer_date ≤ estimated_delivery_date` | percepção do cliente |
| **Frete %** | mediana de `freight_value / price` **por pedido** | reflete o pedido típico; `price=0` → nulo |
| NPS-proxy (seller) | `% reviews ≥ 4` | proxy de promotores |
| RFM | quartis de Recência (invertida), Frequência, Monetário | segmentação |

## 6. KPIs consolidados (valores apurados)
Gerados em `outputs/*.csv`. Principais:

| KPI | Valor |
|---|---|
| Pedidos entregues (escopo) | 96.478 (não entregues: 2.963, excluídos) |
| Clientes únicos | 93.358 |
| Receita total (GMV, c/ frete) | ~R$ 15,7 mi |
| Ticket médio (mercadoria, s/ frete) | R$ 137,42 (desvio mensal R$ 7,44 → estável) |
| YoY receita (jan–ago 17→18) | +140% |
| Black Friday (nov/17) | 1,36× a média do trimestre |
| Share Sudeste / SP | 64,6% / 37,4% |
| Categorias p/ 80% da receita | 18 |
| Sellers p/ 80% da receita | 558 (de 3.053 ativos) |
| Top 20 sellers / top 20 produtos | 20,9% / 5,2% da receita |
| Entregas no prazo | 93,2% |
| Nota média (no prazo × atraso) | 4,29 × 2,27 |
| Taxa de recompra | 3,0% |
| Receita via cartão | 78,3% |
| Rotas críticas de frete (>35%, mediana por pedido) | RR, RO, MA, AM, AC, PB |
| Não entregues (excluídos) — receita em risco | R$ 370,1 mil produto + R$ 53,6 mil frete |
| Atraso × satisfação (Welch t-test) | queda ~2 estrelas, p≈0 (nacional, NE e CO) |
| Simulação descentralização 30% (NE+CO) | 4.209 pedidos · 169 atrasos evitados · R$ 51,2 mil economia de frete |
| Recompra 90 dias / share recorrentes / top-20% ABC | 2,0% / 5,5% / 56,6% |
| Qualidade de dados | 166 postagens e 23 transportes com intervalo negativo; 8 delivered sem data |

## 7. Saídas geradas
- **`figs/`** — PNGs por frente, prefixados `p1_`…`p4_` (22 gráficos).
- **`outputs/`** — CSVs de KPIs e tabelas auxiliares por frente (`pN_*.csv`).
- **`notebooks/`** — 4 notebooks executados com saídas embutidas.

## 8. Limitações conhecidas
- Série temporal curta (~2 anos) → previsão limitada a média móvel/tendência, não modelo sazonal robusto.
- Dataset sem nome de produto (só `product_id` + categoria) → top produtos rotulados por categoria + id.
- `payment_value` (pagamentos) pode divergir de `price+freight` (vouchers, parcelamento) → receita usa itens.
- Reviews sem análise de sentimento de texto nesta fase (campo disponível para evolução futura).
- Recompra subestimável se houver múltiplos `customer_unique_id` para a mesma pessoa (limitação do dado).

"""
Fabrica de notebooks - helpers compartilhados para gerar os .ipynb da entrega.
Cada gerador (gen_pessoaN.py) importa daqui.

Uso:
    import build_common as bc
    cells = [bc.md("# Titulo"), bc.code("print('oi')")]
    bc.write_and_run(cells, "notebooks/01_xxx.ipynb")
"""
from pathlib import Path
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

REPO = Path(__file__).resolve().parent.parent   # .../tech_challenge_olist


def md(text: str):
    return new_markdown_cell(text)


def code(src: str):
    return new_code_cell(src)


# ---------------------------------------------------------------------------
# Bloco de SETUP padrao (carga + escopo canonico). Reusado em todos os notebooks.
# ---------------------------------------------------------------------------
SETUP_IMPORTS = r'''
# === Setup: imports e tema visual ===
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# Localiza a raiz do projeto (onde existe a pasta data/)
ROOT = Path.cwd()
for cand in [ROOT, *ROOT.parents]:
    if (cand / "data" / "olist_orders_dataset.csv").exists():
        ROOT = cand; break
DATA_DIR = ROOT / "data"
FIG_DIR  = ROOT / "figs";    FIG_DIR.mkdir(exist_ok=True, parents=True)
OUT_DIR  = ROOT / "outputs"; OUT_DIR.mkdir(exist_ok=True, parents=True)

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({
    "figure.figsize": (12, 6), "figure.dpi": 100, "savefig.dpi": 150,
    "savefig.bbox": "tight", "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
})
# Paleta Darwin / Olist
ROSA, PRETO, TEAL, AMARELO, AZUL, CINZA = "#de0078","#1f1f1f","#00a3a1","#ffb800","#5b6bf5","#8c8c8c"
PALETTE = [ROSA, TEAL, AMARELO, AZUL, CINZA, PRETO]

def brl(x, _=None):
    return f"R$ {x:,.0f}".replace(",", ".")
print("Projeto:", ROOT)
'''

SETUP_LOAD = r'''
# === Carga dos 9 datasets do Olist ===
def load(name):
    df = pd.read_csv(DATA_DIR / name)
    return df

orders    = load("olist_orders_dataset.csv")
items     = load("olist_order_items_dataset.csv")
payments  = load("olist_order_payments_dataset.csv")
reviews   = load("olist_order_reviews_dataset.csv")
products  = load("olist_products_dataset.csv")
customers = load("olist_customers_dataset.csv")
sellers   = load("olist_sellers_dataset.csv")
cat_trans = load("product_category_name_translation.csv")

ts_cols = ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date",
           "order_delivered_customer_date","order_estimated_delivery_date"]
for c in ts_cols:
    orders[c] = pd.to_datetime(orders[c], errors="coerce")

print(f"orders={orders.shape} | items={items.shape} | payments={payments.shape} | reviews={reviews.shape}")
print(f"Janela de compra: {orders['order_purchase_timestamp'].min().date()} -> {orders['order_purchase_timestamp'].max().date()}")
'''

SETUP_SCOPE = r'''
# === Escopo canonico: APENAS pedidos ENTREGUES (delivered) ===
# Decisao de escopo: usamos somente pedidos efetivamente entregues. Os casos nao
# entregues (shipped/invoiced/processing/canceled/unavailable/...) sao mostrados
# separadamente no ADENDO e excluidos da analise -- so os entregues tem data de
# entrega, frete realizado e review confiaveis.
ESCOPO_STATUS = "delivered"
orders_v = orders[orders["order_status"] == ESCOPO_STATUS].copy()
orders_v["year_month"] = orders_v["order_purchase_timestamp"].dt.to_period("M")

# Convencao do projeto (duas metricas distintas, NAO confundir):
#  - gross_price   = valor da MERCADORIA do pedido (soma dos precos dos itens)  -> base do TICKET MEDIO
#  - order_revenue = gross_price + frete (GMV recebido pela plataforma)         -> base da RECEITA/FATURAMENTO
# Ticket medio considera APENAS o produto (sem frete). Frete entra so como variavel propria.
items_rev = (items.groupby("order_id")
                  .agg(gross_price=("price","sum"),
                       freight=("freight_value","sum"),
                       n_items=("order_item_id","count"))
                  .reset_index())
items_rev["order_revenue"] = items_rev["gross_price"] + items_rev["freight"]

orders_v = orders_v.merge(items_rev, on="order_id", how="left")
orders_v = orders_v.merge(
    customers[["customer_id","customer_unique_id","customer_state","customer_city"]],
    on="customer_id", how="left")
orders_v["lead_time_dias"] = (orders_v["order_delivered_customer_date"]
                              - orders_v["order_purchase_timestamp"]).dt.days
# Frete como % do preco, calculado POR PEDIDO (a mediana disso = frete do pedido tipico)
orders_v["frete_pct_pedido"] = orders_v["freight"] / orders_v["gross_price"].replace(0, np.nan)

# Tabela de itens enriquecida (categoria PT->EN, UF cliente, UF seller)
items_full = (items.merge(products[["product_id","product_category_name"]], on="product_id", how="left")
                   .merge(cat_trans, on="product_category_name", how="left")
                   .merge(orders_v[["order_id","year_month","customer_state","customer_city"]], on="order_id", how="inner")
                   .merge(sellers[["seller_id","seller_state","seller_city"]], on="seller_id", how="left"))
items_full["revenue"] = items_full["price"] + items_full["freight_value"]
items_full["cat"] = (items_full["product_category_name_english"]
                     .fillna("sem_categoria").str.replace("_"," ").str.title())

print(f"Escopo: APENAS pedidos entregues (delivered)")
print(f"Pedidos entregues: {orders_v['order_id'].nunique():,}")
print(f"Clientes unicos:   {orders_v['customer_unique_id'].nunique():,}")
print(f"Receita total (GMV c/ frete): R$ {orders_v['order_revenue'].sum():,.2f}")
print(f"Ticket medio (mercadoria):    R$ {orders_v['gross_price'].mean():,.2f}")
print(f"Frete % do preco (mediana por pedido): {orders_v['frete_pct_pedido'].median():.1%}")
'''


def setup_section(extra_intro_md: str = ""):
    """Retorna as celulas padrao de setup que abrem cada notebook."""
    cells = []
    cells.append(md("## 0. Setup, carga e escopo\n\n"
                    "Bloco reprodutível idêntico em todos os notebooks: carrega os 9 datasets do Olist, define o "
                    "**escopo canônico — apenas pedidos entregues (`delivered`)** — e enriquece a tabela de itens "
                    "com categoria traduzida e UF de cliente/seller. Os pedidos **não entregues** são tratados no "
                    "adendo e excluídos da análise.\n\n"
                    "> **Convenção de métricas:** _ticket médio_ = valor da **mercadoria** (`price`, sem frete); "
                    "_receita/faturamento_ = `price + frete` (GMV); _frete %_ = mediana do `frete/price` **por pedido**.\n\n"
                    + extra_intro_md))
    cells.append(code(SETUP_IMPORTS.strip()))
    cells.append(code(SETUP_LOAD.strip()))
    cells.append(code(SETUP_SCOPE.strip()))
    return cells


def write_and_run(cells, rel_path: str, run: bool = True, timeout: int = 600):
    """Monta o notebook, salva e (opcional) executa embutindo as saidas."""
    nb = new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3.12 (Olist)", "language": "python", "name": "olist312"},
        "language_info": {"name": "python", "version": "3.12"},
    })
    out = REPO / rel_path
    out.parent.mkdir(exist_ok=True, parents=True)
    if run:
        ep = ExecutePreprocessor(timeout=timeout, kernel_name="olist312")
        ep.preprocess(nb, {"metadata": {"path": str(out.parent)}})
    with open(out, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"OK -> {out.relative_to(REPO)}  ({len(cells)} celulas, executado={run})")
    return out

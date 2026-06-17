# -*- coding: utf-8 -*-
"""Gera o grafico de satisfacao x cumprimento da promessa de entrega (foco geografico NE/CO/Sul)."""
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"; FIG = ROOT / "figs"; OUT = ROOT / "outputs"
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({"figure.dpi":100,"savefig.dpi":150,"savefig.bbox":"tight",
                     "axes.titleweight":"bold","axes.spines.top":False,"axes.spines.right":False})
ROSA,PRETO,TEAL,AMARELO,AZUL,CINZA = "#de0078","#1f1f1f","#00a3a1","#ffb800","#5b6bf5","#8c8c8c"

REGIAO = {"AC":"Norte","AP":"Norte","AM":"Norte","PA":"Norte","RO":"Norte","RR":"Norte","TO":"Norte",
 "AL":"Nordeste","BA":"Nordeste","CE":"Nordeste","MA":"Nordeste","PB":"Nordeste","PE":"Nordeste","PI":"Nordeste","RN":"Nordeste","SE":"Nordeste",
 "DF":"Centro-Oeste","GO":"Centro-Oeste","MT":"Centro-Oeste","MS":"Centro-Oeste",
 "ES":"Sudeste","MG":"Sudeste","RJ":"Sudeste","SP":"Sudeste","PR":"Sul","RS":"Sul","SC":"Sul"}
COR_REG = {"Nordeste":ROSA,"Centro-Oeste":AMARELO,"Sul":TEAL,"Sudeste":CINZA,"Norte":AZUL}
FOCO = ["Nordeste","Centro-Oeste","Sul"]

# --- dados
o = pd.read_csv(D/"olist_orders_dataset.csv")
c = pd.read_csv(D/"olist_customers_dataset.csv")
r = pd.read_csv(D/"olist_order_reviews_dataset.csv")[["order_id","review_score"]].drop_duplicates("order_id")
for col in ["order_purchase_timestamp","order_delivered_customer_date","order_estimated_delivery_date"]:
    o[col] = pd.to_datetime(o[col], errors="coerce")
o = o[o["order_status"]=="delivered"].merge(c[["customer_id","customer_state"]],on="customer_id",how="left")
o = o.merge(r, on="order_id", how="inner")
o["atraso"] = (o["order_delivered_customer_date"]-o["order_estimated_delivery_date"]).dt.days
o = o.dropna(subset=["atraso","review_score"])
o["regiao"] = o["customer_state"].map(REGIAO)
o["no_prazo"] = o["atraso"] <= 0

fig, ax = plt.subplots(1, 2, figsize=(17, 7))

# ====== Painel A: nota media por faixa de cumprimento da promessa, por regiao ======
faixas = ["Adiantado\n(>3 dias)","No prazo\n(±3 dias)","Atrasado\n(3-10 dias)","Muito atrasado\n(>10 dias)"]
def faixa(a):
    if a < -3: return faixas[0]
    if a <= 3: return faixas[1]
    if a <= 10: return faixas[2]
    return faixas[3]
o["faixa"] = o["atraso"].apply(faixa)
piv = (o[o["regiao"].isin(FOCO)].groupby(["faixa","regiao"])["review_score"].mean()
       .unstack().reindex(faixas))
x = np.arange(len(faixas)); w = 0.26
for i, reg in enumerate(FOCO):
    ax[0].bar(x + (i-1)*w, piv[reg].values, w, label=reg, color=COR_REG[reg])
ax[0].axhline(o["review_score"].mean(), color=PRETO, ls="--", lw=1.5,
              label=f"média Brasil {o['review_score'].mean():.2f}")
ax[0].set_xticks(x); ax[0].set_xticklabels(faixas, fontsize=11)
ax[0].set_ylabel("Nota média de review"); ax[0].set_ylim(1, 5)
ax[0].set_title("Satisfação × cumprimento da promessa de entrega\n(regiões foco)")
ax[0].legend(fontsize=11, loc="lower left")

# ====== Painel B: scatter por UF — % no prazo x nota media ======
uf = (o.groupby("customer_state")
        .agg(nota=("review_score","mean"), no_prazo=("no_prazo","mean"),
             pedidos=("order_id","count")).reset_index())
uf["regiao"] = uf["customer_state"].map(REGIAO)
for reg, sub in uf.groupby("regiao"):
    ax[1].scatter(sub["no_prazo"]*100, sub["nota"], s=sub["pedidos"]/15+40,
                  color=COR_REG[reg], alpha=.85, edgecolor="white", lw=1.2,
                  label=reg + (" (foco)" if reg in FOCO else ""))
for _, row in uf.iterrows():
    ax[1].annotate(row["customer_state"], (row["no_prazo"]*100, row["nota"]),
                   fontsize=8.5, ha="center", va="center")
ax[1].axhline(o["review_score"].mean(), color=PRETO, ls=":", alpha=.5)
ax[1].set_xlabel("% de entregas dentro da promessa")
ax[1].set_ylabel("Nota média de review")
ax[1].set_title("Cada UF: cumprir a promessa puxa a satisfação\n(bolha = nº de pedidos)")
ax[1].legend(fontsize=10, loc="lower right", title="Região")

plt.tight_layout()
plt.savefig(FIG/"geo_satisfacao_promessa.png"); plt.close()

# baseline por regiao (export)
base = (o.groupby("regiao").agg(nota_media=("review_score","mean"),
        pct_no_prazo=("no_prazo",lambda s:s.mean()*100),
        pct_detratores=("review_score",lambda s:(s<=2).mean()*100),
        pedidos=("order_id","count")).round(2)
        .reindex(["Norte","Nordeste","Centro-Oeste","Sudeste","Sul"]))
base.to_csv(OUT/"baseline_satisfacao_regiao.csv")
print("OK -> figs/geo_satisfacao_promessa.png")
print(base.to_string())

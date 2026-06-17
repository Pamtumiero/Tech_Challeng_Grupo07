# -*- coding: utf-8 -*-
"""Diagnostico geografico: (Q1) por que NE/CO compram menos; (Q2) gargalo da promessa de entrega."""
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
D = ROOT/"data"; FIG = ROOT/"figs"; OUT = ROOT/"outputs"
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({"figure.dpi":100,"savefig.dpi":150,"savefig.bbox":"tight",
                     "axes.titleweight":"bold","axes.spines.top":False,"axes.spines.right":False})
ROSA,PRETO,TEAL,AMARELO,AZUL,CINZA = "#de0078","#1f1f1f","#00a3a1","#ffb800","#5b6bf5","#8c8c8c"
COR={"Norte":AZUL,"Nordeste":ROSA,"Centro-Oeste":AMARELO,"Sudeste":CINZA,"Sul":TEAL}
REG={**dict.fromkeys(["AC","AP","AM","PA","RO","RR","TO"],"Norte"),
 **dict.fromkeys(["AL","BA","CE","MA","PB","PE","PI","RN","SE"],"Nordeste"),
 **dict.fromkeys(["DF","GO","MT","MS"],"Centro-Oeste"),
 **dict.fromkeys(["ES","MG","RJ","SP"],"Sudeste"),
 **dict.fromkeys(["PR","RS","SC"],"Sul")}
ordem=["Norte","Nordeste","Centro-Oeste","Sudeste","Sul"]

o=pd.read_csv(D/"olist_orders_dataset.csv")
c=pd.read_csv(D/"olist_customers_dataset.csv")
it=pd.read_csv(D/"olist_order_items_dataset.csv")
s=pd.read_csv(D/"olist_sellers_dataset.csv")
for col in ["order_purchase_timestamp","order_approved_at","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]:
    o[col]=pd.to_datetime(o[col],errors="coerce")

rev=it.groupby("order_id").agg(preco=("price","sum"),frete=("freight_value","sum")).reset_index()
rev["receita"]=rev["preco"]+rev["frete"]
# escopo: apenas entregues (consistente com o resto da analise)
ov=o[o["order_status"]=="delivered"].merge(c[["customer_id","customer_state"]],on="customer_id",how="left").merge(rev,on="order_id",how="left")
ov["regiao"]=ov["customer_state"].map(REG); ov["frete_pct"]=ov["frete"]/ov["preco"].replace(0,np.nan)
s["regiao_seller"]=s["seller_state"].map(REG)
sellers_reg=s.groupby("regiao_seller")["seller_id"].nunique()

g=ov.dropna(subset=["preco"]).groupby("regiao").agg(
    pedidos=("order_id","nunique"), ticket=("preco","mean"),
    frete_pct=("frete_pct","median")).reindex(ordem)
g["sellers"]=sellers_reg.reindex(ordem)
g["frete_pct"]*=100

# ===== FIG Q1 =====
fig,ax=plt.subplots(1,2,figsize=(17,7))
x=np.arange(len(ordem))
ax[0].bar(x-0.2, g["pedidos"], 0.4, label="Pedidos (cliente)", color=PRETO)
ax[0].bar(x+0.2, g["sellers"], 0.4, label="Sellers locais (oferta)", color=ROSA)
ax[0].set_yscale("log"); ax[0].set_xticks(x); ax[0].set_xticklabels(ordem, rotation=15)
ax[0].set_ylabel("Escala log"); ax[0].set_title("Demanda existe, oferta local não\nPedidos × sellers locais por região")
ax[0].legend(fontsize=12)
for i,(p,se) in enumerate(zip(g["pedidos"],g["sellers"])):
    ax[0].text(i+0.2, se*1.15, f"{int(se)}", ha="center", fontsize=10, color=ROSA, weight="bold")

for i,reg in enumerate(ordem):
    ax[1].scatter(g.loc[reg,"frete_pct"], g.loc[reg,"ticket"], s=g.loc[reg,"pedidos"]/25+80,
                  color=COR[reg], edgecolor="white", lw=1.5, alpha=.9)
    ax[1].annotate(reg, (g.loc[reg,"frete_pct"], g.loc[reg,"ticket"]),
                   textcoords="offset points", xytext=(8,6), fontsize=12, weight="bold")
ax[1].set_xlabel("Frete mediano por pedido (% do preço)"); ax[1].set_ylabel("Ticket médio · mercadoria (R$)")
ax[1].set_title("Frete alto filtra a compra:\nsó pedido caro 'compensa' o frete")
ax[1].xaxis.set_major_formatter(mtick.PercentFormatter())
plt.tight_layout(); plt.savefig(FIG/"geo_q1_oferta_frete.png"); plt.close()

# ===== FIG Q2: decomposicao lead time =====
d=o[o["order_status"]=="delivered"].merge(c[["customer_id","customer_state"]],on="customer_id",how="left")
d["regiao"]=d["customer_state"].map(REG)
d["t_postagem"]=(d["order_delivered_carrier_date"]-d["order_purchase_timestamp"]).dt.total_seconds()/86400
d["t_transporte"]=(d["order_delivered_customer_date"]-d["order_delivered_carrier_date"]).dt.total_seconds()/86400
d["atraso"]=(d["order_delivered_customer_date"]-d["order_estimated_delivery_date"]).dt.days
dd=d.dropna(subset=["t_postagem","t_transporte"])
q=dd.groupby("regiao").agg(t_postagem=("t_postagem","median"),
    t_transporte=("t_transporte","median"),
    no_prazo=("atraso",lambda x:(x<=0).mean()*100)).reindex(ordem)

fig,ax=plt.subplots(figsize=(13,7))
x=np.arange(len(ordem))
ax.bar(x, q["t_postagem"], color=AMARELO, label="Compra → postagem (seller)")
ax.bar(x, q["t_transporte"], bottom=q["t_postagem"], color=ROSA, label="Postagem → cliente (transporte)")
ax.set_xticks(x); ax.set_xticklabels(ordem)
ax.set_ylabel("Dias (mediana)")
ax.set_title("Onde o tempo é perdido: o gargalo é o TRANSPORTE, não o seller")
for i,reg in enumerate(ordem):
    tot=q.loc[reg,"t_postagem"]+q.loc[reg,"t_transporte"]
    ax.text(i, tot+0.4, f"{tot:.0f}d\n{q.loc[reg,'no_prazo']:.0f}% no prazo", ha="center", fontsize=11, weight="bold")
ax.legend(fontsize=12)
plt.tight_layout(); plt.savefig(FIG/"geo_q2_gargalo_entrega.png"); plt.close()

g.round(1).to_csv(OUT/"geo_diagnostico_regiao.csv")
q.round(1).to_csv(OUT/"geo_decomposicao_leadtime.csv")
print("OK -> figs/geo_q1_oferta_frete.png, figs/geo_q2_gargalo_entrega.png")

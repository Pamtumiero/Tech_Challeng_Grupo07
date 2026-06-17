# -*- coding: utf-8 -*-
"""Atraso de entrega: sellers LOCAIS (mesma regiao do cliente) vs NAO-LOCAIS. Escopo: delivered."""
from pathlib import Path
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).resolve().parent.parent
D=ROOT/"data"; FIG=ROOT/"figs"; OUT=ROOT/"outputs"
sns.set_theme(style="whitegrid", context="talk")
plt.rcParams.update({"figure.dpi":100,"savefig.dpi":150,"savefig.bbox":"tight",
                     "axes.titleweight":"bold","axes.spines.top":False,"axes.spines.right":False})
ROSA,PRETO,TEAL,AMARELO,AZUL,CINZA="#de0078","#1f1f1f","#00a3a1","#ffb800","#5b6bf5","#8c8c8c"
REG={**dict.fromkeys(["AC","AP","AM","PA","RO","RR","TO"],"Norte"),
 **dict.fromkeys(["AL","BA","CE","MA","PB","PE","PI","RN","SE"],"Nordeste"),
 **dict.fromkeys(["DF","GO","MT","MS"],"Centro-Oeste"),
 **dict.fromkeys(["ES","MG","RJ","SP"],"Sudeste"),
 **dict.fromkeys(["PR","RS","SC"],"Sul")}

o=pd.read_csv(D/"olist_orders_dataset.csv")
c=pd.read_csv(D/"olist_customers_dataset.csv")
it=pd.read_csv(D/"olist_order_items_dataset.csv")
s=pd.read_csv(D/"olist_sellers_dataset.csv")
for col in ["order_purchase_timestamp","order_delivered_carrier_date","order_delivered_customer_date","order_estimated_delivery_date"]:
    o[col]=pd.to_datetime(o[col],errors="coerce")
o=o[o["order_status"]=="delivered"].merge(c[["customer_id","customer_state"]],on="customer_id",how="left")
o["creg"]=o["customer_state"].map(REG)
it2=it.merge(s[["seller_id","seller_state"]],on="seller_id",how="left"); it2["sreg"]=it2["seller_state"].map(REG)
oc=o[["order_id","creg"]].merge(it2[["order_id","sreg"]],on="order_id",how="inner").dropna(subset=["creg","sreg"])
# pedido local = TODOS os sellers na mesma regiao do cliente
g=oc.groupby("order_id").apply(lambda d:(d["sreg"]==d["creg"].iloc[0]).all(), include_groups=False).rename("local").reset_index()
o=o.merge(g,on="order_id",how="inner")
o["lead"]=(o["order_delivered_customer_date"]-o["order_purchase_timestamp"]).dt.days
o["atraso"]=(o["order_delivered_customer_date"]-o["order_estimated_delivery_date"]).dt.days
o=o.dropna(subset=["lead","atraso"]); o["tipo"]=np.where(o["local"],"Local","Não-local")

ORDEM=["Nordeste","Centro-Oeste","Sul","Sudeste"]
agg=(o[o["creg"].isin(ORDEM)].groupby(["creg","tipo"])
     .agg(pedidos=("order_id","size"), lead=("lead","median"),
          no_prazo=("atraso",lambda x:(x<=0).mean()*100)).reset_index())

fig,ax=plt.subplots(1,2,figsize=(17,6.5))
x=np.arange(len(ORDEM)); w=0.38
for j,(tipo,cor) in enumerate([("Local",TEAL),("Não-local",ROSA)]):
    sub=agg[agg["tipo"]==tipo].set_index("creg").reindex(ORDEM)
    ax[0].bar(x+(j-0.5)*w, sub["lead"], w, label=tipo, color=cor)
    for i,(v,n) in enumerate(zip(sub["lead"],sub["pedidos"])):
        if pd.notna(v): ax[0].text(x[i]+(j-0.5)*w, v+0.2, f"{v:.0f}d\nn={int(n):,}".replace(",","."), ha="center", fontsize=9)
ax[0].set_xticks(x); ax[0].set_xticklabels(ORDEM); ax[0].set_ylabel("Lead time mediano (dias)")
ax[0].set_title("Prazo de entrega: seller LOCAL vs NÃO-LOCAL"); ax[0].legend()
for j,(tipo,cor) in enumerate([("Local",TEAL),("Não-local",ROSA)]):
    sub=agg[agg["tipo"]==tipo].set_index("creg").reindex(ORDEM)
    ax[1].bar(x+(j-0.5)*w, sub["no_prazo"], w, label=tipo, color=cor)
    for i,v in enumerate(sub["no_prazo"]):
        if pd.notna(v): ax[1].text(x[i]+(j-0.5)*w, v+0.4, f"{v:.0f}%", ha="center", fontsize=9, weight="bold")
ax[1].set_xticks(x); ax[1].set_xticklabels(ORDEM); ax[1].set_ylabel("% entregas no prazo"); ax[1].set_ylim(80,100)
ax[1].set_title("Cumprimento da promessa: LOCAL vs NÃO-LOCAL"); ax[1].legend()
plt.tight_layout(); plt.savefig(FIG/"geo_q2_local_vs_naolocal.png"); plt.close()

# export
tab=(o.groupby(["creg","tipo"]).agg(pedidos=("order_id","size"), lead_mediana=("lead","median"),
     pct_no_prazo=("atraso",lambda x:(x<=0).mean()*100)).round(1)
     .reindex(["Norte","Nordeste","Centro-Oeste","Sudeste","Sul"],level=0))
tab.to_csv(OUT/"geo_local_vs_naolocal.csv")
ger=(o.groupby("tipo").agg(pedidos=("order_id","size"), lead_mediana=("lead","median"),
     pct_no_prazo=("atraso",lambda x:(x<=0).mean()*100)).round(1))
print("GERAL:\n", ger.to_string())
print("\nfig -> geo_q2_local_vs_naolocal.png")

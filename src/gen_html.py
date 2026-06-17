# -*- coding: utf-8 -*-
"""Relatorio executivo HTML autocontido - FOCADO no problema 'Geografia e Categorias'.
Consolida todos os estudos a servico de uma unica tese geografica."""
import base64, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figs"
OUT = ROOT / "relatorio_executivo_olist.html"


def img(name, alt=""):
    p = FIG / name
    if not p.exists():
        return f'<div class="missing">[{name} não encontrado]</div>'
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f'<figure><img src="data:image/png;base64,{b64}" alt="{alt}"><figcaption>{alt}</figcaption></figure>'

CSS = """
:root{--rosa:#de0078;--preto:#1f1f1f;--teal:#00a3a1;--amarelo:#ffb800;--azul:#5b6bf5;
--cinza:#8c8c8c;--claro:#f6f3f4;--bg:#ffffff;--txt:#23202a}
*{box-sizing:border-box}
body{margin:0;font-family:'Segoe UI',Inter,system-ui,Arial,sans-serif;color:var(--txt);background:var(--bg);line-height:1.6;font-size:16px}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
header.hero{background:var(--preto);color:#fff;padding:64px 0 52px;border-bottom:6px solid var(--rosa)}
header.hero h1{font-size:2.5rem;margin:0 0 8px;font-weight:800;letter-spacing:-.5px}
header.hero .sub{color:var(--rosa);font-weight:700;font-size:1.1rem;margin-bottom:6px}
header.hero .meta{color:#b9b9b9;font-size:.95rem}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:34px 0 4px}
.kpi{background:#2a2a2a;border-radius:14px;padding:20px 16px;text-align:center}
.kpi .v{font-size:1.7rem;font-weight:800;color:#fff}
.kpi .v.rosa{color:var(--rosa)}.kpi .v.teal{color:var(--teal)}.kpi .v.amarelo{color:var(--amarelo)}
.kpi .l{font-size:.8rem;color:#c8c8c8;margin-top:4px}
section{padding:46px 0;border-bottom:1px solid #eee}
.tag{display:inline-block;background:var(--rosa);color:#fff;font-size:.74rem;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:.4px;text-transform:uppercase}
.tag.teal{background:var(--teal)}.tag.preto{background:var(--preto)}.tag.azul{background:var(--azul)}
h2{font-size:1.7rem;margin:14px 0 6px;font-weight:800;letter-spacing:-.3px}
h3{font-size:1.15rem;margin:26px 0 8px;color:var(--preto)}
.lead{color:#555;font-size:1.05rem;margin:0 0 18px;max-width:82ch}
figure{margin:18px 0;background:var(--claro);border-radius:12px;padding:14px;border:1px solid #ececec}
figure img{width:100%;height:auto;border-radius:6px;display:block}
figcaption{font-size:.85rem;color:var(--cinza);text-align:center;margin-top:8px;font-style:italic}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
ul.ins{list-style:none;padding:0;margin:16px 0}
ul.ins li{padding:10px 0 10px 34px;position:relative;border-bottom:1px dashed #eee}
ul.ins li::before{content:"▸";position:absolute;left:8px;color:var(--rosa);font-weight:800}
ul.ins li b{color:var(--preto)}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:.92rem}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #eee;vertical-align:top}
th{background:var(--preto);color:#fff;font-weight:600}
tr:nth-child(even) td{background:var(--claro)}
.callout{background:linear-gradient(90deg,#fff5fb,#fff);border-left:5px solid var(--rosa);padding:16px 20px;border-radius:0 10px 10px 0;margin:20px 0;font-size:1rem}
.callout b{color:var(--rosa)}
.regioes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0}
.reg{border-radius:12px;padding:16px;border:1px solid #ececec;background:var(--claro)}
.reg h4{margin:0 0 6px;font-size:1.05rem}.reg p{margin:0;font-size:.9rem;color:#555}
.reg.foco{border-left:5px solid var(--rosa)}.reg.bench{border-left:5px solid var(--teal)}.reg.rest{border-left:5px solid var(--azul)}
.toc{background:var(--claro);border-radius:12px;padding:18px 24px;margin:26px 0;font-size:.95rem}
.toc a{color:var(--preto);text-decoration:none;font-weight:600}.toc a:hover{color:var(--rosa)}
.missing{color:#b00;font-size:.8rem}
footer{padding:40px 0;color:var(--cinza);font-size:.85rem}
@media(max-width:780px){.kpis,.grid2,.regioes{grid-template-columns:1fr 1fr}header.hero h1{font-size:1.8rem}}
"""

html = f"""<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Olist · Geografia e Categorias — Tech Challenge Fase 1</title>
<style>{CSS}</style></head><body>

<header class="hero"><div class="wrap">
  <div class="sub">Tech Challenge Fase 1 · POSTECH DTAT · Análise de dados</div>
  <h1>Geografia e Categorias: destravar o Brasil além do Sudeste1</h1>
  <div class="meta">Brazilian E-Commerce Public Dataset by Olist · set/2016–set/2018 · Lucas Moura · Pamela Costa · Guilherme Silva · Mariana Zeron · Vitor Martino</div>
  <div class="kpis">
    <div class="kpi"><div class="v rosa">64,6%</div><div class="l">da receita no Sudeste</div></div>
    <div class="kpi"><div class="v amarelo">56 / 79</div><div class="l">sellers locais no NE / CO</div></div>
    <div class="kpi"><div class="v">31%</div><div class="l">frete sobre o preço no NE</div></div>
    <div class="kpi"><div class="v teal">3,97</div><div class="l">nota do NE (a menor do país)</div></div>
  </div>
</div></header>

<div class="wrap">

<section id="sumario">
  <span class="tag preto">Sumário executivo</span>
  <h2>O problema e a tese</h2>
  <p class="lead">A Olist é, na prática, um e-commerce do <b>Sudeste</b> (64,6% da receita). O crescimento futuro
  está em destravar as outras regiões — mas elas se comportam de formas opostas. Esta análise responde a duas
  perguntas de negócio e mostra que ambas têm <b>a mesma causa raiz</b>.</p>
  <div class="regioes">
    <div class="reg rest"><h4>🟦 Norte — restrição</h4><p>Barreira <b>geográfica</b> (rios, falta de estradas).
      Reconhecida, mas fora do alcance da empresa. Não é o foco da solução.</p></div>
    <div class="reg foco"><h4>🟥 Nordeste / 🟨 Centro-Oeste — foco</h4><p>Há demanda premium reprimida.
      É onde a intervenção tem retorno: <b>o problema a resolver</b>.</p></div>
    <div class="reg bench"><h4>🟩 Sul — benchmark</h4><p>A região "fora do Sudeste" que <b>deu certo</b>.
      Mostra o que é possível quando a oferta está perto.</p></div>
  </div>
  <div class="toc"><b>Navegação:</b>&nbsp;
    <a href="#adendo">Adendo · escopo</a> &nbsp;·&nbsp;
    <a href="#panorama">1 · Panorama</a> &nbsp;·&nbsp;
    <a href="#q1">2 · Q1 — por que compram menos</a> &nbsp;·&nbsp;
    <a href="#categorias">3 · Categorias por região</a> &nbsp;·&nbsp;
    <a href="#q2">4 · Q2 — promessa de entrega</a> &nbsp;·&nbsp;
    <a href="#sintese">5 · Síntese &amp; recomendações</a>
  </div>
  <div class="callout"><b>Tese:</b> o mapa de receita da Olist não é destino — é <b>consequência de onde a oferta
  está</b>. NE e CO compram pouco <i>e</i> recebem atrasado pela mesma razão: não há vendedor por perto.
  Aproximar a oferta resolve os dois.</div>
</section>

<section id="adendo">
  <span class="tag preto">Adendo · escopo</span>
  <h2>Usamos apenas pedidos <i>entregues</i></h2>
  <p class="lead">Antes dos números, o recorte: <b>toda a análise usa exclusivamente os pedidos com status
  <code>delivered</code></b> (efetivamente entregues). Os pedidos <b>não entregues</b> aparecem aqui de forma
  transparente e são <b>excluídos</b> das análises seguintes — só os entregues têm data de entrega, frete
  realizado e avaliação confiáveis.</p>
  {img('geo_adendo_status.png','Pedidos entregues (usados) vs. não entregues (excluídos) e o detalhamento dos excluídos')}
  <table><tr><th>Grupo</th><th>Pedidos</th><th>Uso</th></tr>
    <tr><td><b>Entregues (delivered)</b></td><td><b>96.478</b> (97,0%)</td><td>✔ base de toda a análise</td></tr>
    <tr><td>Não entregues</td><td>2.963 (3,0%)</td><td>✖ excluídos (detalhe abaixo)</td></tr>
    <tr><td style="padding-left:28px">· enviado (em trânsito)</td><td>1.107</td><td>sem data de entrega/review</td></tr>
    <tr><td style="padding-left:28px">· cancelado</td><td>625</td><td>não virou venda</td></tr>
    <tr><td style="padding-left:28px">· indisponível</td><td>609</td><td>não virou venda</td></tr>
    <tr><td style="padding-left:28px">· faturado / em processamento / criado / aprovado</td><td>622</td><td>ainda no funil</td></tr>
  </table>
  <div class="callout"><b>Por que excluir:</b> um pedido <code>shipped</code> ou <code>processing</code> ainda não
  gerou frete realizado nem avaliação; <code>canceled</code>/<code>unavailable</code> nunca viraram venda. Manter
  só os <code>delivered</code> garante que <b>todo número se refere a uma transação completa e auditável</b> —
  e é o critério que fixa o Nordeste em <b>9.044 pedidos</b>.</div>

  <h3>Quanto custa e por que falharam</h3>
  <p class="lead">Os não entregues não são pedidos "em andamento" — são <b>falhas reais</b>: mediana de 9–13 meses
  de idade, prazo prometido já vencido em ~100% e nota de review péssima (1,3–2,0).</p>
  <ul class="ins">
    <li><b>🚚 Perdido no transporte — <code>shipped</code> (37%):</b> pago e postado, nunca chegou. O <b>mesmo elo frágil do Q2</b>; pior no NE (não-entrega 3,73% vs 2,36% no Sul).</li>
    <li><b>📦 Sem estoque — <code>unavailable</code> (21%):</b> pago, produto não existia. <b>Pior nota (1,5)</b> — falha de catálogo do seller.</li>
    <li><b>⏳ Travado — <code>invoiced</code>/<code>processing</code> (21%):</b> pago e o vendedor nunca despachou — falha de fulfillment.</li>
    <li><b>❌ Cancelado (21%):</b> 88% antes de postar; 12% já postados (desistência por atraso).</li>
  </ul>
  <div class="callout"><b>Impacto: ~R$ 370 mil de produto + R$ 53,6 mil de frete em receita em risco</b> (parte
  é reembolsada). Aponta um <b>segundo problema, operacional</b>, ao lado do geográfico: integridade de estoque e
  SLA de fulfillment. <span class="muted">Governança: 166 registros com postagem e 23 com transporte em intervalos
  fisicamente impossíveis foram sinalizados.</span></div>
</section>

<section id="panorama">
  <span class="tag">1 · Panorama</span>
  <h2>O tamanho do problema</h2>
  <p class="lead">A receita é hiperconcentrada no Sudeste, e o ticket de mercadoria <b>sobe</b> à medida que a
  região se afasta do Sudeste — o primeiro sinal de que algo filtra a compra nas regiões distantes.</p>
  {img('geo_00_panorama.png','Participação na receita e ticket médio (mercadoria) por região')}
  <p>Do lado das <b>categorias</b>, a receita se espalha por uma cauda longa saudável — 18 categorias somam 80%.
  Nenhuma domina, o que significa que destravar uma região exige levar um <b>sortimento amplo</b>, não 2-3 itens.</p>
  {img('geo_01_categorias.png','Top categorias por receita — concentração saudável (cauda longa)')}
</section>

<section id="q1">
  <span class="tag">2 · Q1</span>
  <h2>Por que Nordeste e Centro-Oeste compram menos que o Sul?</h2>
  <p class="lead">A resposta não é falta de demanda — é <b>falta de oferta local</b>. A oferta (sellers) está no
  Sudeste; NE/CO importam quase tudo, o frete dispara e <b>filtra a compra</b>: só o pedido caro compensa.</p>
  {img('geo_q1_oferta_frete.png','Oferta local escassa (esq.) e o frete filtrando a compra (dir.)')}
  <ul class="ins">
    <li><b>Oferta concentrada:</b> NE tem <b>56</b> sellers e CO <b>79</b>, contra <b>668 no Sul</b> e 2.287 no Sudeste.</li>
    <li><b>Frete como pedágio:</b> no pedido típico o frete é ~<b>31% do preço no NE</b> e ~25% no CO (20% no Sudeste).</li>
    <li><b>O efeito-filtro:</b> NE/CO têm o <b>maior ticket de mercadoria do país</b> (R$ 166 / R$ 151) — só vale
      pagar o frete em pedidos caros; as compras pequenas, que dão volume ao Sul, evaporam.</li>
    <li><b>Por isso o Sul compra mais:</b> oferta perto (668 sellers) + colado no Sudeste → frete e prazo viáveis.</li>
  </ul>
</section>

<section id="categorias">
  <span class="tag azul">3 · Categorias × Região</span>
  <h2>O que cada região compra — e o que isso revela</h2>
  <p class="lead">As regiões têm preferências distintas. O mapa abaixo mostra o quanto cada categoria pesa
  <b>acima ou abaixo</b> da média nacional em cada região — e a leitura confirma a tese do frete.</p>
  {img('geo_02_categoria_overindex.png','Sobre/sub-indexação de categorias por região vs. média nacional')}
  <ul class="ins">
    <li><b>O NE foge das categorias pesadas:</b> Bed Bath Table (−45%), Housewares (−39%), Furniture (−19%) —
      itens volumosos, em que o frete é proibitivo. A categoria conta a mesma história do frete.</li>
    <li><b>E sobre-indexa em itens pequenos de alto valor:</b> Health Beauty (+41%), Auto (+28%), Watches Gifts
      (+22%) — leves, caros, "valem" o frete. É a <b>demanda premium reprimida</b> visível no sortimento.</li>
    <li><b>O Sul parece o Sudeste:</b> compra móveis e decoração (Furniture +29%) porque o frete viabiliza o volumoso.</li>
    <li><b>Implicação:</b> as categorias verdes do NE/CO são as apostas seguras para recrutar sellers locais e montar bundles regionais.</li>
  </ul>
</section>

<section id="q2">
  <span class="tag">4 · Q2</span>
  <h2>O que melhorar para cumprir a promessa de entrega?</h2>
  <p class="lead">Decompondo o prazo em <b>postagem do seller</b> e <b>transporte</b>, o gargalo aparece com
  clareza — e não é onde a intuição aponta.</p>
  {img('geo_q2_gargalo_entrega.png','Decomposição do prazo: o gargalo é o transporte, não o seller')}
  <ul class="ins">
    <li><b>O seller despacha rápido e por igual</b> em todo o Brasil (~2 dias). Pressionar SLA de seller <b>não move</b> NE/CO.</li>
    <li><b>A diferença é 100% transporte:</b> 6 dias no Sudeste → <b>14 dias no Nordeste</b> — a perna de longa distância.</li>
    <li><b>NE tem o pior cumprimento de promessa (87%)</b> porque essa perna é a mais <b>variável</b> — difícil de prometer com precisão.</li>
  </ul>

  <h3>4a · Vendedor local entrega melhor — e onde mais importa, mais</h3>
  <p class="lead">Classificando cada pedido como <b>local</b> (vendedor na mesma região do cliente) ou <b>não-local</b>:
  se a origem da oferta é a causa, o local deve ser mais rápido e pontual. E é.</p>
  {img('geo_q2_local_vs_naolocal.png','Lead time e % no prazo: vendedor local vs. não-local, por região')}
  <ul class="ins">
    <li><b>No agregado, o local entrega ~5 dias mais rápido</b> (8 vs 13 dias).</li>
    <li><b>Nordeste:</b> local 11d / 91% no prazo vs. não-local 17d / 87%.</li>
    <li><b>Centro-Oeste:</b> local 7d / <b>98%</b> vs. não-local 13d / 93% — quase perfeito.</li>
    <li><b>Prova empírica:</b> onde já existe oferta local, a entrega já é rápida e cumpre a promessa.</li>
  </ul>

  <h3>4b · Por que o NE demora mesmo <i>local</i>? Distância — não o vendedor</h3>
  <p class="lead">O pedido "local" do NE ainda leva ~12 dias porque <b>"local" = mesma região, e o Nordeste é enorme</b>
  (9 estados). Abrindo o NE em etapas e em mesmo-estado × outro-estado, a causa fica inequívoca.</p>
  {img('geo_q2_distancia_ne.png','NE por distância: a postagem é constante, o transporte cresce; same-state ≈ Sudeste')}
  <ul class="ins">
    <li><b>A postagem é constante (~2 dias)</b> em todos os recortes; o que cresce é o <b>transporte</b>.</li>
    <li><b>A maioria dos pedidos "locais" do NE cruza estados</b> (ex.: BA→MA) e leva ~13 dias.</li>
    <li><b>No mesmo estado, o NE entrega em 7 dias — igual ao Sudeste (6,5d).</b> Não há nada intrinsecamente lento no NE.</li>
  </ul>
  <div class="callout"><b>Isto refina a recomendação:</b> não basta um <b>hub único</b> no Nordeste — cruzar estados
  internos já custa ~6 dias. O alvo é <b>fulfillment distribuído nos estados-âncora de demanda (BA, PE, CE)</b>,
  maximizando a fatia de pedidos <i>same-state</i>. <span class="muted">(Ressalva: o n de same-state no NE é pequeno
  — 135 — porque hoje quase não há vendedor local; o mecanismo de distância, porém, é claro.)</span></div>

  <h3>Por que isso importa: a satisfação segue a promessa</h3>
  <p class="lead">Cumprir a promessa <b>é</b> o que sustenta a nota. A baseline regional define a linha de partida —
  e o Nordeste é a maior alavanca.</p>
  {img('geo_satisfacao_promessa.png','Satisfação × cumprimento da promessa, por faixa de atraso e por UF')}
  <table><tr><th>Região</th><th>Nota média</th><th>% no prazo</th><th>% detratores (1–2)</th></tr>
    <tr><td><b>🟥 Nordeste</b></td><td>3,97</td><td>87,5%</td><td>16,7%</td></tr>
    <tr><td><b>🟨 Centro-Oeste</b></td><td>4,13</td><td>93,6%</td><td>13,2%</td></tr>
    <tr><td><b>🟩 Sul</b></td><td>4,19</td><td>94,2%</td><td>11,8%</td></tr>
    <tr><td style="color:#8c8c8c">Sudeste (referência)</td><td>4,18</td><td>94,0%</td><td>12,4%</td></tr>
  </table>
  <h3>O atraso <i>causa</i> a queda? Teste estatístico (Welch t-test)</h3>
  <p class="lead">Para não depender só da diferença de médias, um <b>Welch t-test</b> compara a nota de pedidos
  no prazo vs. atrasados. Se o p-valor é baixo, o atraso é um detrator real — não ruído amostral.</p>
  <table><tr><th>Recorte</th><th>Nota no prazo</th><th>Nota atrasado</th><th>Queda</th><th>p-valor</th></tr>
    <tr><td>Nacional</td><td>4,29</td><td>2,27</td><td><b>−2,02</b></td><td>≈ 0</td></tr>
    <tr><td><b>Nordeste</b></td><td>4,23</td><td>2,18</td><td><b>−2,04</b></td><td>1,7 × 10⁻²⁵¹</td></tr>
    <tr><td><b>Centro-Oeste</b></td><td>4,26</td><td>2,18</td><td><b>−2,08</b></td><td>9,2 × 10⁻⁸⁶</td></tr>
  </table>
  <p>Queda de <b>~2 estrelas</b> com p-valor praticamente nulo em todos os recortes → diferença
  <b>estatisticamente significante</b>. O atraso é, comprovadamente, o maior detrator individual da experiência.</p>
</section>

<section id="sintese">
  <span class="tag preto">5 · Síntese &amp; Recomendações</span>
  <h2>Uma causa raiz, dois sintomas</h2>
  <table>
    <tr><th></th><th>Q1 — compram menos</th><th>Q2 — entrega atrasa</th></tr>
    <tr><td><b>Sintoma</b></td><td>volume baixo no NE/CO</td><td>promessa furada, nota baixa (NE 3,97)</td></tr>
    <tr><td><b>Mecanismo</b></td><td>sem seller local → frete alto → filtra a compra</td><td>sem origem local → transporte longo e variável</td></tr>
    <tr><td><b>Causa raiz</b></td><td colspan="2" style="text-align:center"><b>oferta (sellers/estoque) longe do cliente</b></td></tr>
  </table>
  <div class="callout"><b>Colocar oferta dentro do NE/CO ataca os dois ao mesmo tempo:</b> baixa o frete (mais
  compras) <i>e</i> encurta o transporte (cumpre a promessa). Uma alavanca, dois problemas resolvidos.</div>

  <h3>Recomendações geográficas — com metas de satisfação</h3>
  <p>Foco em NE e CO (Norte = restrição reconhecida; Sul = manter). Métrica-norte: <b>satisfação média regional</b>.</p>
  <table><tr><th>#</th><th>Ação</th><th>Resolve</th><th>Meta (partida → alvo)</th><th>Prazo</th></tr>
    <tr><td>1</td><td><b>Fulfillment distribuído nos estados-âncora</b> (BA, PE, CE) — <i>não</i> um hub único</td><td>Q1 frete + Q2 transporte</td><td>NE nota 3,97 → <b>4,15</b> · no prazo 87% → <b>93%</b> · ↑ <i>same-state</i></td><td>90–180d</td></tr>
    <tr><td>2</td><td><b>Recrutar sellers locais NE/CO</b> nas categorias que sobre-indexam</td><td>Q1 oferta/frete</td><td>NE sellers 56 → <b>150+</b>, espalhados por estado</td><td>6–12m</td></tr>
    <tr><td>3</td><td><b>Transportadora regional dedicada</b> no corredor Sudeste→NE/CO <b>e intra-NE</b></td><td>Q2 transporte</td><td>CO 93,6% → <b>95%</b></td><td>90d</td></tr>
    <tr><td>4</td><td><b>Bundles regionais</b> nas categorias de sobre-indexação</td><td>Q1 ticket/volume</td><td>itens/pedido NE/CO ↑</td><td>30–60d</td></tr>
    <tr><td>5</td><td><b>Recalibrar data prometida por rota</b> (tático)</td><td>Q2 promessa</td><td>quebra de promessa NE ↓</td><td>30d</td></tr>
  </table>
  <h3>O que NÃO fazer</h3>
  <ul class="ins">
    <li><b>Não</b> apostar num <b>hub único</b> no NE — cruzar estados internos ainda custa ~6 dias; o alvo é distribuir perto da demanda.</li>
    <li><b>Não</b> prometer prazos agressivos no NE antes de ter oferta local — atraso destrói a nota.</li>
    <li><b>Não</b> tratar o Norte como NE — lá a barreira é geográfica (rios/estradas), fora do alcance da empresa.</li>
    <li><b>Não</b> pressionar SLA de seller esperando ganho de prazo — o vendedor posta em 2 dias, não é o gargalo.</li>
  </ul>
  <h3>Quanto isso vale: simulação do cenário 30%</h3>
  <p>Cenário-base: migrar <b>30% dos pedidos hoje despachados de fora da região</b> para sourcing local,
  aplicando o desempenho já observado nos pedidos locais. Números próprios (cenário, não previsão).</p>
  <table><tr><th>Região</th><th>Pedidos migrados (30%)</th><th>Atrasos evitados</th><th>Economia de frete</th></tr>
    <tr><td>Nordeste</td><td>2.584</td><td>92</td><td>R$ 35.812</td></tr>
    <tr><td>Centro-Oeste</td><td>1.625</td><td>77</td><td>R$ 15.429</td></tr>
    <tr><td><b>Total</b></td><td><b>4.209</b></td><td><b>169</b></td><td><b>R$ 51.241</b></td></tr>
  </table>
  <p>~169 atrasos evitados e ~R$ 51 mil de economia de frete/ano-base — capital que <b>financia a própria
  atração de sellers locais</b> (recomendação #2). Os pedidos migrados ganham ~<b>+0,3 estrela</b>, elevando satisfação e recompra.</p>

  <div class="callout"><b>Mensagem ao board:</b> a prova de que dá para resolver está no dado — onde o vendedor é do
  <b>mesmo estado</b>, o NE entrega em 7 dias, igual ao Sudeste. Aproximar a oferta — <b>distribuída nos estados de
  maior demanda</b>, não num hub único — converte a demanda premium já existente <b>e</b> cumpre a promessa, medido
  pela <b>satisfação</b> dessas regiões.</div>
</section>

<footer><div class="wrap" style="padding:0">
  <p><b>Metodologia.</b> <b>Escopo:</b> apenas pedidos entregues (<code>delivered</code>, 96.478) — não entregues
  excluídos (ver adendo). <b>Ticket médio</b> = valor da mercadoria (<code>price</code>, sem frete);
  <b>receita</b> = preço + frete (GMV); <b>frete %</b> = mediana do <code>frete/preço</code> por pedido.
  Cliente único por <code>customer_unique_id</code>.
  Análise central no notebook <code>02_geografia_categorias.ipynb</code>; estudos de apoio (crescimento, top
  performers, profundidade/RFM) nos notebooks 01, 03 e 04. Pipeline reprodutível em Python 3.12 / pandas 2.2.
  Fonte: Brazilian E-Commerce Public Dataset by Olist (Kaggle).</p>
  <p>Tech Challenge Fase 1 · POSTECH DTAT · 2026<br>
  Lucas Aguiar de Moura (RM375551) · Pamela Regina Tumiero da Costa (RM374909) · Guilherme Augusto Justino da Silva (RM374370) · Mariana Nogueira Salgado Zeron (RM374774) · Vitor Martino (RM374436)</p>
</div></footer>

</div></body></html>"""

OUT.write_text(html, encoding="utf-8")
print(f"OK -> {OUT.name}  ({len(html)//1024} KB, autocontido, foco geográfico)")

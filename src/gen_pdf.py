# -*- coding: utf-8 -*-
"""Gera o relatorio em PDF (ABNT + identidade FIAP) — reportlab, reusando as figuras geo_*."""
from pathlib import Path
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                PageBreak, KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figs"
OUT = ROOT / "apresentacao" / "Relatorio_Tech_Challenge_Olist_ABNT_FIAP.pdf"

MAG = colors.HexColor("#ED145B")
PRETO = colors.HexColor("#1A1A1A")
BR = "Helvetica"; BRB = "Helvetica-Bold"; BRI = "Helvetica-Oblique"
CW = 16.0  # largura util aprox (21 - 3 - 2 = 16 cm)

S = {
    "body": ParagraphStyle("body", fontName=BR, fontSize=12, leading=18, alignment=TA_JUSTIFY,
                           firstLineIndent=1.25*cm, spaceAfter=6, textColor=PRETO),
    "body0": ParagraphStyle("body0", fontName=BR, fontSize=12, leading=18, alignment=TA_JUSTIFY,
                            spaceAfter=6, textColor=PRETO),
    "h1": ParagraphStyle("h1", fontName=BRB, fontSize=13, leading=16, textColor=MAG,
                         spaceBefore=14, spaceAfter=8),
    "bul": ParagraphStyle("bul", fontName=BR, fontSize=11, leading=16, alignment=TA_JUSTIFY,
                          leftIndent=1.0*cm, bulletIndent=0.4*cm, spaceAfter=3, textColor=PRETO),
    "capfig": ParagraphStyle("capfig", fontName=BRB, fontSize=10, leading=12, alignment=TA_CENTER, spaceBefore=8),
    "fonte": ParagraphStyle("fonte", fontName=BR, fontSize=9, leading=11, alignment=TA_CENTER,
                            textColor=colors.grey, spaceAfter=10),
    "ctr": ParagraphStyle("ctr", fontName=BR, fontSize=12, leading=16, alignment=TA_CENTER, textColor=PRETO),
    "ctrb": ParagraphStyle("ctrb", fontName=BRB, fontSize=12, leading=16, alignment=TA_CENTER, textColor=PRETO),
    "titcapa": ParagraphStyle("titcapa", fontName=BRB, fontSize=18, leading=24, alignment=TA_CENTER, textColor=MAG),
    "subcapa": ParagraphStyle("subcapa", fontName=BRI, fontSize=12, leading=16, alignment=TA_CENTER, textColor=PRETO),
    "nota": ParagraphStyle("nota", fontName=BR, fontSize=11, leading=16, alignment=TA_JUSTIFY,
                           leftIndent=8*cm, textColor=PRETO),
    "tcell": ParagraphStyle("tcell", fontName=BR, fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=PRETO),
    "thead": ParagraphStyle("thead", fontName=BRB, fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=colors.white),
    "resumo": ParagraphStyle("resumo", fontName=BR, fontSize=12, leading=18, alignment=TA_JUSTIFY, textColor=PRETO, spaceAfter=6),
}

story = []
_fig = {"n": 0}

def P(txt, st="body"): return Paragraph(txt, S[st])
def H(txt): return Paragraph(txt, S["h1"])  # capturado no TOC via afterFlowable
def BUL(txt): return Paragraph(txt, S["bul"], bulletText="•")
def SP(h=6): return Spacer(1, h)

def figura(arquivo, titulo, fonte="Elaborado pelos autores (2026), a partir do dataset Olist (Kaggle)."):
    _fig["n"] += 1
    p = FIG / arquivo
    iw, ih = PILImage.open(p).size
    w = CW*cm; h = w*ih/iw
    img = Image(str(p), width=w, height=h)
    return KeepTogether([Paragraph(f"Figura {_fig['n']} — {titulo}", S["capfig"]), img,
                         Paragraph(f"Fonte: {fonte}", S["fonte"])])

def tabela(headers, rows, larguras_cm, titulo, num):
    data = [[Paragraph(h, S["thead"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S["tcell"]) for c in r])
    t = Table(data, colWidths=[w*cm for w in larguras_cm], repeatRows=1, hAlign="CENTER")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),MAG),
        ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#BBBBBB")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#FCEAF1")]),
    ]))
    return KeepTogether([t, Paragraph(f"Tabela {num} — {titulo}", S["capfig"]),
                         Paragraph("Fonte: Elaborado pelos autores (2026).", S["fonte"])])

# ===================== CAPA =====================
story += [SP(6),
    Paragraph("FACULDADE DE INFORMÁTICA E ADMINISTRAÇÃO PAULISTA — FIAP", S["ctrb"]),
    Paragraph("Pós-Graduação (POSTECH) — Data Analytics", S["ctr"]), SP(150),
    Paragraph("GEOGRAFIA E CATEGORIAS:", S["titcapa"]),
    Paragraph("DESTRAVAR O BRASIL ALÉM DO SUDESTE", S["titcapa"]), SP(12),
    Paragraph("Diagnóstico geográfico-logístico do marketplace Olist e proposta de descentralização da oferta", S["subcapa"]),
    SP(200), Paragraph("Tech Challenge — Fase 1", S["ctrb"]), SP(40),
    Paragraph("São Paulo", S["ctrb"]), Paragraph("2026", S["ctrb"]), PageBreak()]

# ===================== FOLHA DE ROSTO =====================
story += [SP(6),
    Paragraph("Lucas Aguiar de Moura — RM375551", S["ctrb"]),
    Paragraph("Pamela Regina Tumiero da Costa — RM374909", S["ctrb"]),
    Paragraph("Guilherme Augusto Justino da Silva — RM374370", S["ctrb"]),
    Paragraph("Mariana Nogueira Salgado Zeron — RM374774", S["ctrb"]),
    Paragraph("Vitor Martino — RM374436", S["ctrb"]), SP(120),
    Paragraph("GEOGRAFIA E CATEGORIAS:", S["titcapa"]),
    Paragraph("DESTRAVAR O BRASIL ALÉM DO SUDESTE", S["titcapa"]), SP(50),
    Paragraph("Relatório técnico-analítico apresentado como requisito de avaliação do Tech Challenge Fase 1 do "
              "curso de Pós-Graduação em Data Analytics da FIAP, com base no Brazilian E-Commerce Public Dataset "
              "by Olist.", S["nota"]), SP(180),
    Paragraph("São Paulo", S["ctrb"]), Paragraph("2026", S["ctrb"]), PageBreak()]

# ===================== RESUMO =====================
story += [H("RESUMO"),
    P("Este relatório investiga o problema geográfico do marketplace Olist: por que as regiões fora do Sudeste "
      "compram menos e recebem com mais atraso, e o que fazer a respeito. Sobre 96.478 pedidos efetivamente "
      "entregues (set/2016–ago/2018), demonstra-se que a concentração da oferta no Sudeste (64,6% da receita) é "
      "a causa raiz comum de dois sintomas: (i) o frete elevado — mediana de 31,5% do preço no Nordeste — "
      "filtra a compra de menor valor; e (ii) a perna de transporte de longa distância estoura o prazo prometido. "
      "Mostra-se, por decomposição do lead time e por teste de hipótese (Welch t-test, p≈0), que o gargalo é o "
      "transporte — não o vendedor — e que, no mesmo estado, o Nordeste entrega tão rápido quanto o Sudeste "
      "(7 dias). Conclui-se com uma proposta de descentralização da oferta, cujo cenário de 30% projeta ~169 "
      "atrasos evitados e ~R$ 51 mil de economia de frete.", "resumo"),
    SP(8), Paragraph("<b>Palavras-chave:</b> e-commerce; logística; análise geográfica; satisfação do cliente; Olist.", S["body0"]),
    PageBreak()]

# ===================== SUMÁRIO =====================
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle("toc1", fontName=BR, fontSize=12, leading=20, leftIndent=0)]
story += [H("SUMÁRIO"), toc, PageBreak()]

# ===================== 1 INTRODUÇÃO =====================
story += [H("1 INTRODUÇÃO"),
    P("A Olist é um integrador de marketplaces que conecta milhares de pequenos e médios vendedores (sellers) aos "
      "grandes portais de e-commerce do Brasil. Em aproximadamente dois anos, a plataforma movimentou cerca de "
      "R$ 13,2 milhões em mercadoria sobre 96.478 pedidos entregues. Apesar do crescimento expressivo, a operação é "
      "fortemente concentrada na Região Sudeste, o que levanta a questão central deste trabalho: como destravar o "
      "potencial de consumo das demais regiões do país."),
    P("Duas perguntas de negócio orientam a análise: (1) por que Nordeste e Centro-Oeste compram menos que o Sul? e "
      "(2) o que pode ser melhorado para cumprir as promessas de prazo de entrega? Demonstra-se que ambas "
      "compartilham a mesma causa raiz — a localização da oferta —, o que conduz a uma recomendação única e "
      "mensurável.")]

# ===================== 2 METODOLOGIA =====================
story += [H("2 METODOLOGIA"),
    P("A base utilizada é o Brazilian E-Commerce Public Dataset by Olist (Kaggle), composto por nove tabelas "
      "relacionais. O processamento foi conduzido em Python 3.12 (pandas, matplotlib, scipy), de forma "
      "integralmente reprodutível. Definições e decisões de escopo adotadas:", "body0"),
    BUL("<b>Escopo:</b> utilizam-se exclusivamente os pedidos com status <i>delivered</i> (entregues). Os não "
        "entregues são tratados em adendo e excluídos das métricas."),
    BUL("<b>Ticket médio:</b> valor da mercadoria (<i>price</i>), sem o frete — métrica de comportamento de compra."),
    BUL("<b>Receita/faturamento:</b> <i>price</i> + frete (GMV recebido pela plataforma)."),
    BUL("<b>Frete (%):</b> mediana da razão frete/preço calculada <b>por pedido</b> (pedido típico, robusta a outliers)."),
    BUL("Macrorregiões pela UF do cliente; análise local×não-local pela UF do vendedor.")]

# ===================== 3 PANORAMA =====================
story += [H("3 PANORAMA: A CONCENTRAÇÃO NO SUDESTE"),
    P("A receita é hiperconcentrada no Sudeste (64,6%), e o ticket médio de mercadoria cresce à medida que a região "
      "se afasta do Sudeste — primeiro indício de que algo filtra a compra nas regiões distantes (Figura 1)."),
    figura("geo_00_panorama.png", "Participação na receita e ticket médio (mercadoria) por região"),
    P("Do lado das categorias, a receita distribui-se por uma cauda longa saudável — 18 categorias respondem por "
      "80% do faturamento, sem dependência de um único nicho (Figura 2)."),
    figura("geo_01_categorias.png", "Categorias com maior receita (concentração saudável)")]

# ===================== 4 Q1 =====================
story += [H("4 POR QUE NORDESTE E CENTRO-OESTE COMPRAM MENOS (Q1)"),
    P("A resposta não é falta de demanda, e sim falta de oferta local. O Nordeste conta com apenas 56 vendedores "
      "locais e o Centro-Oeste com 79, contra 668 no Sul e 2.287 no Sudeste. Como quase tudo é despachado de longe, "
      "o frete torna-se um pedágio: no pedido típico equivale a ~31% do preço no Nordeste e ~25% no Centro-Oeste, "
      "contra ~20% no Sudeste (Figura 3)."),
    figura("geo_q1_oferta_frete.png", "Oferta local escassa (esq.) e o frete filtrando a compra (dir.)"),
    P("O efeito é um filtro de compra: NE e CO exibem o maior ticket de mercadoria do país (R$ 165 e R$ 150) não por "
      "maior poder aquisitivo, mas porque só vale a pena pagar o frete em pedidos caros — as compras pequenas, "
      "que dão volume ao Sul, deixam de acontecer.")]

# ===================== 5 CATEGORIAS =====================
story += [H("5 CATEGORIAS POR REGIÃO"),
    P("As regiões têm preferências distintas, e a leitura confirma a tese do frete. O Nordeste sub-indexa em "
      "categorias volumosas — cama, mesa e banho (−45%) e utilidades domésticas (−39%) — nas quais "
      "o frete é proibitivo, e sobre-indexa em itens pequenos e de alto valor — saúde e beleza (+41%), relógios e "
      "presentes (+22%) e acessórios automotivos (+28%) —, que “compensam” o frete (Figura 4)."),
    figura("geo_02_categoria_overindex.png", "Sobre/sub-indexação de categorias por região vs. média nacional")]

# ===================== 6 Q2 =====================
story += [H("6 O QUE MELHORAR NA ENTREGA (Q2)"),
    P("Decompondo o prazo em postagem (vendedor) e transporte (transportadora), o gargalo fica evidente: a postagem "
      "é praticamente constante (~2 dias) em todo o país, enquanto o transporte salta de 6 dias no Sudeste para 14 "
      "dias no Nordeste (Figura 5)."),
    figura("geo_q2_gargalo_entrega.png", "Decomposição do prazo: o gargalo é o transporte, não o vendedor"),
    P("A origem da oferta confirma o mecanismo: pedidos de vendedor local entregam ~5 dias mais rápido no agregado. "
      "No Nordeste, o pedido local leva 11 dias (91% no prazo) contra 17 do não-local (87%); no Centro-Oeste, 7 dias "
      "(98%) contra 13 (93%) — Figura 6."),
    figura("geo_q2_local_vs_naolocal.png", "Prazo e cumprimento de promessa: vendedor local vs. não-local"),
    P("Por que o Nordeste demora mesmo quando “local”? Porque “local” é a mesma região, e o Nordeste é "
      "geograficamente enorme. A maioria dos pedidos locais do NE cruza estados (ex.: BA→MA, ~13,5 dias). Quando "
      "vendedor e cliente estão no mesmo estado, o NE entrega em 7 dias — igual ao Sudeste (6,5). Ou seja: o "
      "problema é a distância, não o vendedor (Figura 7)."),
    figura("geo_q2_distancia_ne.png", "Nordeste por distância: same-state entrega como o Sudeste")]

# ===================== 7 SATISFAÇÃO + WELCH =====================
story += [H("7 SATISFAÇÃO E A PROVA ESTATÍSTICA"),
    P("A satisfação segue diretamente o cumprimento da promessa de entrega. A baseline regional posiciona o "
      "Nordeste como a maior alavanca: menor nota média (3,97) e maior proporção de detratores (16,7%) — Figura 8."),
    figura("geo_satisfacao_promessa.png", "Satisfação × cumprimento da promessa, por faixa de atraso e por UF"),
    P("Para confirmar a causalidade, aplicou-se o teste de Welch comparando a nota de pedidos no prazo versus "
      "atrasados. Em todos os recortes, a queda é de aproximadamente 2 estrelas, com p-valor praticamente nulo "
      "— diferença estatisticamente significante (Tabela 1)."),
    tabela(["Recorte","Nota no prazo","Nota atrasado","Queda","p-valor"],
           [["Nacional","4,29","2,27","−2,02","≈ 0"],
            ["Nordeste","4,23","2,18","−2,04","1,7 × 10<super>-251</super>"],
            ["Centro-Oeste","4,26","2,18","−2,08","9,2 × 10<super>-86</super>"]],
           [3.5,3.0,3.0,2.5,4.0], "Teste de Welch: nota no prazo vs. atrasado", 1)]

# ===================== 8 ADENDO =====================
story += [H("8 ADENDO: OS PEDIDOS NÃO ENTREGUES"),
    P("Dos 99.441 pedidos da base, 2.963 (3,0%) não foram entregues e ficaram fora da análise. Não se trata de "
      "truncamento — são falhas reais (idade mediana de 9 a 13 meses, prazo prometido vencido e notas de 1,3 a "
      "2,0). Distribuem-se em quatro modos de falha (Figura 9)."),
    figura("geo_adendo_status.png", "Pedidos entregues (usados) vs. não entregues (excluídos), por status"),
    BUL("<b>Perdido no transporte</b> (shipped, 37%): pago e postado, nunca chegou; pior no Nordeste (3,73% vs. 2,36% no Sul)."),
    BUL("<b>Sem estoque</b> (unavailable, 21%): pago, produto inexistente — pior nota (1,5)."),
    BUL("<b>Travado no funil</b> (invoiced/processing, 21%): pago e nunca despachado."),
    BUL("<b>Cancelado</b> (21%): majoritariamente antes da postagem; 12% já postados."),
    P("O impacto é de ~R$ 370,1 mil em mercadoria e R$ 53,6 mil em frete em receita em risco, apontando um segundo "
      "problema, de natureza operacional (integridade de estoque e SLA de fulfillment), ao lado do geográfico.")]

# ===================== 9 SIMULAÇÃO =====================
story += [H("9 SIMULAÇÃO DO CENÁRIO DE DESCENTRALIZAÇÃO (30%)"),
    P("Modelou-se a migração de 30% dos pedidos hoje despachados de fora da região para sourcing local, aplicando "
      "aos migrados o desempenho já observado nos pedidos locais. Trata-se de um cenário-base, não de previsão "
      "(Tabela 2)."),
    tabela(["Região","Pedidos migrados (30%)","Atrasos evitados","Economia de frete"],
           [["Nordeste","2.584","92","R$ 35.812"],["Centro-Oeste","1.625","77","R$ 15.429"],
            ["Total","4.209","169","R$ 51.241"]],
           [4.0,4.5,3.5,4.0], "Simulação de descentralização de 30% (NE + CO)", 2),
    P("A economia de frete financia a própria atração de sellers locais; e os pedidos migrados ganham cerca de "
      "+0,3 estrela de nota média, elevando a satisfação e a probabilidade de recompra.")]

# ===================== 10 RECOMENDAÇÕES =====================
story += [H("10 RECOMENDAÇÕES"),
    P("Foco em Nordeste e Centro-Oeste (o Norte é restrição geográfica, fora do alcance privado; o Sul deve ser "
      "mantido). Métrica-norte: satisfação média regional (Tabela 3)."),
    tabela(["#","Ação","Resolve","Meta","Prazo"],
           [["1","Fulfillment distribuído nos estados-âncora (BA, PE, CE) — não um hub único","Q1+Q2","NE 3,97→4,15; prazo 87%→93%","90–180d"],
            ["2","Recrutar sellers locais NE/CO nas categorias que sobre-indexam","Q1","NE 56→150+","6–12m"],
            ["3","Transportadora regional dedicada (corredor e intra-NE)","Q2","CO 93,6%→95%","90d"],
            ["4","Bundles regionais nas categorias de sobre-indexação","Q1","↑ itens/pedido","30–60d"],
            ["5","Recalibrar a data prometida por rota (tático)","Q2","↓ quebra de promessa","30d"]],
           [0.8,6.0,1.8,4.2,2.2], "Recomendações com metas de satisfação", 3)]

# ===================== 11 CONSIDERAÇÕES FINAIS =====================
story += [H("11 CONSIDERAÇÕES FINAIS"),
    P("O mapa de receita da Olist não é um destino, e sim a consequência de onde a oferta está localizada. Nordeste "
      "e Centro-Oeste compram pouco e recebem com atraso pela mesma razão — a ausência de vendedores próximos. A "
      "prova está nos próprios dados: onde o vendedor é do mesmo estado, o Nordeste entrega em sete dias, igual ao "
      "Sudeste. Aproximar a oferta — de forma distribuída pelos estados de maior demanda, e não em um hub único "
      "— converte a demanda premium já existente e cumpre a promessa de entrega, medido pelo indicador que mais "
      "importa para a marca: a satisfação dessas regiões.")]

# ===================== REFERÊNCIAS =====================
story += [PageBreak(), H("REFERÊNCIAS")]
for ref in [
    "KAGGLE. Brazilian E-Commerce Public Dataset by Olist. Disponível em: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Acesso em: jun. 2026.",
    "CHOPRA, S.; MEINDL, P. Gestão da cadeia de suprimentos: estratégia, planejamento e operação. 6. ed. São Paulo: Pearson, 2016.",
    "PROVOST, F.; FAWCETT, T. Data science para negócios. Rio de Janeiro: Alta Books, 2016.",
]:
    story.append(Paragraph(ref, ParagraphStyle("ref", fontName=BR, fontSize=11, leading=14,
                 alignment=TA_JUSTIFY, spaceAfter=8, textColor=PRETO)))

# ===================== DOC com TOC + numero de pagina =====================
class DocTOC(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "h1":
            txt = flowable.getPlainText()
            # nao indexar capa/folha; indexa secoes (inclui RESUMO/SUMARIO/REFERENCIAS)
            if txt and txt != "SUMÁRIO":
                self.notify("TOCEntry", (0, txt, self.page))

def _page_num(canvas, doc):
    canvas.saveState(); canvas.setFont(BR, 10); canvas.setFillColor(PRETO)
    canvas.drawRightString(A4[0]-2*cm, A4[1]-1.5*cm, str(doc.page))
    canvas.restoreState()

doc = DocTOC(str(OUT), pagesize=A4, topMargin=3*cm, leftMargin=3*cm, bottomMargin=2*cm, rightMargin=2*cm,
             title="Relatório Tech Challenge Olist — Geografia e Categorias",
             author="Lucas Aguiar de Moura; Pamela R. T. da Costa; Guilherme A. J. da Silva; Mariana N. S. Zeron; Vitor Martino")
doc.multiBuild(story, onLaterPages=_page_num, onFirstPage=lambda c,d: None)
print(f"OK -> {OUT.relative_to(ROOT)}")

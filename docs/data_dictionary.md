# 📒 Data Dictionary — Brazilian E-Commerce Public Dataset by Olist

Dataset público (Kaggle): pedidos reais de e-commerce no Brasil entre **set/2016 e set/2018**, intermediados
pela Olist. São 9 arquivos CSV relacionáveis por chaves. Diagrama lógico:

```
            customers ──< orders >── order_items >── products ──> category_translation
                            │            │
                            │            └──> sellers
                            ├──> order_payments
                            └──> order_reviews         geolocation (liga por zip_code_prefix)
```

> `>──` = relação 1:N · `──<` = N:1. Granularidades: `orders` = 1 linha por pedido; `order_items` = 1 linha
> por item (um pedido pode ter vários); `payments`/`reviews` = N por pedido.

---

## 1. `olist_orders_dataset.csv` — Pedidos (núcleo)
| Coluna | Tipo | Descrição |
|---|---|---|
| `order_id` | str (PK) | Identificador único do pedido |
| `customer_id` | str (FK) | Liga a `customers` (chave por pedido, não por pessoa) |
| `order_status` | str | `delivered`, `shipped`, `canceled`, `invoiced`, `processing`, `approved`, `unavailable`, `created` |
| `order_purchase_timestamp` | datetime | Momento da compra |
| `order_approved_at` | datetime | Aprovação do pagamento |
| `order_delivered_carrier_date` | datetime | Postagem (entrega à transportadora) |
| `order_delivered_customer_date` | datetime | Entrega ao cliente (real) |
| `order_estimated_delivery_date` | datetime | Data **prometida** ao cliente |

## 2. `olist_order_items_dataset.csv` — Itens do pedido
| Coluna | Tipo | Descrição |
|---|---|---|
| `order_id` | str (FK) | Liga a `orders` |
| `order_item_id` | int | Sequencial do item dentro do pedido (1,2,3…) |
| `product_id` | str (FK) | Liga a `products` |
| `seller_id` | str (FK) | Liga a `sellers` |
| `shipping_limit_date` | datetime | Prazo-limite de postagem do seller |
| `price` | float | Preço do item (R$) |
| `freight_value` | float | Frete do item (R$) |

> **Receita** usada nas análises = `price + freight_value` (GMV recebido pela plataforma).

## 3. `olist_order_payments_dataset.csv` — Pagamentos
| Coluna | Tipo | Descrição |
|---|---|---|
| `order_id` | str (FK) | Liga a `orders` |
| `payment_sequential` | int | Sequência de pagamentos do pedido (split de pagamento) |
| `payment_type` | str | `credit_card`, `boleto`, `voucher`, `debit_card`, `not_defined` |
| `payment_installments` | int | Nº de parcelas |
| `payment_value` | float | Valor pago (R$) |

## 4. `olist_order_reviews_dataset.csv` — Avaliações
| Coluna | Tipo | Descrição |
|---|---|---|
| `review_id` | str | Identificador do review |
| `order_id` | str (FK) | Liga a `orders` |
| `review_score` | int (1–5) | Nota dada pelo cliente |
| `review_comment_title` | str | Título do comentário (opcional) |
| `review_comment_message` | str | Texto do comentário (opcional) |
| `review_creation_date` | datetime | Envio da pesquisa |
| `review_answer_timestamp` | datetime | Resposta do cliente |

## 5. `olist_products_dataset.csv` — Produtos
| Coluna | Tipo | Descrição |
|---|---|---|
| `product_id` | str (PK) | Identificador do produto |
| `product_category_name` | str | Categoria (em português) |
| `product_name_lenght` | int | Nº de caracteres do nome |
| `product_description_lenght` | int | Nº de caracteres da descrição |
| `product_photos_qty` | int | Qtd. de fotos |
| `product_weight_g` | int | Peso (g) |
| `product_length_cm` / `_height_cm` / `_width_cm` | int | Dimensões (cm) |

## 6. `olist_customers_dataset.csv` — Clientes
| Coluna | Tipo | Descrição |
|---|---|---|
| `customer_id` | str (PK) | Chave **por pedido** (liga a `orders`) |
| `customer_unique_id` | str | Identificador **real** da pessoa (use este para recompra/RFM) |
| `customer_zip_code_prefix` | int | Prefixo do CEP |
| `customer_city` | str | Município |
| `customer_state` | str (UF) | Estado de destino |

> ⚠️ **Pegadinha do dataset:** `customer_id` muda a cada pedido. Para contar clientes únicos e recompra,
> use sempre `customer_unique_id`.

## 7. `olist_sellers_dataset.csv` — Vendedores
| Coluna | Tipo | Descrição |
|---|---|---|
| `seller_id` | str (PK) | Identificador do seller |
| `seller_zip_code_prefix` | int | Prefixo do CEP |
| `seller_city` | str | Município |
| `seller_state` | str (UF) | Estado de origem |

## 8. `olist_geolocation_dataset.csv` — Geolocalização
| Coluna | Tipo | Descrição |
|---|---|---|
| `geolocation_zip_code_prefix` | int | Prefixo do CEP (liga a clientes/sellers) |
| `geolocation_lat` / `_lng` | float | Latitude / longitude |
| `geolocation_city` | str | Município |
| `geolocation_state` | str (UF) | Estado |

## 9. `product_category_name_translation.csv` — Tradução de categorias
| Coluna | Tipo | Descrição |
|---|---|---|
| `product_category_name` | str | Categoria em português (liga a `products`) |
| `product_category_name_english` | str | Categoria em inglês (usada nos rótulos) |

---

## Decisões de qualidade e escopo (aplicadas em todos os notebooks)
- **Escopo — apenas entregues:** mantidos **somente** os pedidos `delivered` (96.478). Os não entregues
  (`shipped, invoiced, processing, approved, created, canceled, unavailable` — 2.963 no total) são mostrados
  no **adendo** e excluídos, pois só os entregues têm data de entrega, frete realizado e review confiáveis.
- **Janela analítica:** séries temporais restritas a **jan/2017 – ago/2018** (2016 é início ralo de operação;
  set/2018 está truncado).
- **Receita / faturamento:** `price + freight_value` somados por pedido (GMV, inclui frete).
- **Ticket médio:** apenas `price` (valor da **mercadoria**) por pedido — **não** soma o frete. O frete é
  tratado como variável independente, nunca embutido no ticket.
- **Cliente único:** `customer_unique_id` (nunca `customer_id`).
- **Datas:** convertidas com `pd.to_datetime(errors="coerce")`; nulos de entrega tratados por `dropna` nas
  métricas logísticas.
- **Frete %:** **mediana** de `freight_value / price` calculada **por pedido** (experiência do pedido típico),
  com `price==0` tratado como nulo para evitar divisão por zero.

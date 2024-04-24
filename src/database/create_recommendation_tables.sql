/*=================================================================================*/
/* Table: historico_venda_arquivo                                                  */
/* Descrição: Tabela histórica de arquivos de importação			                    */
/*=================================================================================*/
drop table historico_venda_arquivo;

create table historico_venda_arquivo (
   hvar_id              integer              not null,
   hvar_erp             text                 not null,
   hvar_erp_cliente_id  text                 not null,
   hvar_nome_arquivo    text          	      not null,
   hvar_url             text                 not null,
   hvar_data_envio      timestamp            not null,
   hvar_status          text                 not null,
   hvar_tamanho         decimal              not null,
   constraint PK_HISTORICO_VENDA_ARQUIVO primary key (hvar_id)
);

comment on column historico_venda_arquivo.hvar_erp is
'Nome do ERP que usa o SV Recommender. Exemplo: sv';

comment on column historico_venda_arquivo.hvar_erp_cliente_id is
'ID do Cliente do ERP. Por exemplo: ID do cliente no SV (clie_id)';

comment on column historico_venda_arquivo.hvar_nome_arquivo is
'Nome do arquivo armazenado, a ser processado. Este arquivo será enviado pelo ERP';

comment on column historico_venda_arquivo.hvar_status is
'Não Processado
Processado
Erro';

comment on column historico_venda_arquivo.hvar_tamanho is
'Tamanho do arquivo em KB';

/*=================================================================================*/
/* Table: historico_venda                                                          */
/* Descrição: Tabela histórica de vendas de produtos			                       */
/*=================================================================================*/
drop table historico_venda;
create table historico_venda (
   hive_id                 integer              not null,
   hive_transacao_id       text                 not null,
   hive_consumidor         text                 not null,
   hive_sku                text                 not null,
   hive_data_venda         date                 not null,
   hive_datahora_inclusao  timestamp            null,
   hive_ordem              integer              null,
   hive_valor              decimal              null,
   hive_quantidade         decimal              null,
   hive_fornecedor         text                 not null,
   hive_data_processamento timestamp            null,
   hive_sku_categoria      text                 null,
   hive_status             text                 not null,
   hive_erp_cliente_id     text                 not null,
   hive_erp                text                 not null,
   constraint PK_HISTORICO_VENDA primary key (hive_id)
);

comment on column historico_venda.hive_transacao_id is
'Número do Pedido ou NFe';

comment on column historico_venda.hive_consumidor is
'ID do Consumidor (CNPJ, CPF, COD)';

comment on column historico_venda.hive_sku is
'Código Único do Produto (prod_codigo + cnpj do fornecedor)';

comment on column historico_venda.hive_ordem is
'Ordem que o item foi incluido no pedido ou nfe';

comment on column historico_venda.hive_fornecedor is
'CNPJ do Fornecedor (que fabrica ou fornece o produto)';

comment on column historico_venda.hive_sku_categoria is
'Categoria do Produto';

comment on column historico_venda.hive_status is
'Ativo 
Inativo';

comment on column historico_venda.hive_erp_cliente_id is
'ID/Codigo do Cliente do ERP (clie_id)';

comment on column historico_venda.hive_erp is
'Exemplo: sv';

/*==================================================================================*/
/* Table: recomendacao                                                              */
/* Descrição: Tabela de recomendação de produtos			                           */
/*==================================================================================*/
drop table recomendacao;
create table recomendacao (
   reco_id                      integer              not null,
   reco_erp                     text                 not null,
   reco_erp_cliente_id          text                 not null,
   reco_consumidor              text                 null,
   reco_fornecedor              text                 null,
   reco_sku                     text                 not null,
   reco_hash_sku                text                 not null,
   reco_data_processamento      timestamp            not null,
   reco_sku_recomendacao        json                 not null,
   reco_margem_corte            integer              not null,
   reco_forecast_quantidade     json                 not null,
   reco_forecast_ticket_medio   json                 null,
   reco_forecast_proxima_compra json                 null,
   constraint PK_RECOMENDACAO primary key (reco_id)
);

comment on column recomendacao.reco_consumidor is
'CNPJ, CPF ou COD do Cliente';

comment on column recomendacao.reco_fornecedor is
'CNPJ do Fornecedor';

comment on column recomendacao.reco_sku_recomendacao is
'JSON contendo as recomendações baseado no Cliente ou Global 
(sem considerar o cliente - reco_cliente IS NULL)';

comment on column recomendacao.reco_margem_corte is
'% de recomendação para os produtos.
Exemplo: somente produtos com recomendação acima de 50% serão retornados.';

comment on column recomendacao.reco_erp is
'Exemplo: sv';

comment on column recomendacao.reco_erp_cliente_id is
'ID do Cliente do ERP (clie_id)';

comment on column recomendacao.reco_hash_sku is
'hash de N sku(s) para gerar recomendacoes
erp+erp_cliente_id+consumidor+(skus {}) = HASH

Explico pessoalmente depois.';

comment on column recomendacao.reco_forecast_quantidade is
'registrar o historico de quantidade compradas e forecast para proximas compras 
(armazenar JSON - a especificar)';

comment on column recomendacao.reco_forecast_ticket_medio is
'registrar o historico do valor/preco compradas e forecast para proximas compras 
(armazenar JSON - a especificar)';

comment on column recomendacao.reco_forecast_proxima_compra is
'Calcular o proximo dia provavel de compra... ';
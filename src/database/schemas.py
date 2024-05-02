from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    JSON
)
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

import datetime

# Types 
PrimaryKeyType = UUID(as_uuid=True)
Decimal = NUMERIC(precision=10, scale=2)

Base = declarative_base()    

def get_current_timestamp():
    return datetime.now()

class Provider(Base):
    """
    ERP que usa este serviço. Exemplo: sv
    """
    __tablename__ = "providers"

    prov_id = Column(
        PrimaryKeyType, 
        primary_key=True, 
        index=True,
        comment='ID primário do fornecedor no banco'
    )
    prov_name = Column(String, comment='Nome do ERP que usa o SV Recommender. Exemplo: sv')
    prov_signup_at = Column(
        DateTime, 
        comment='Data e hora do cadastro do fornecedor',
        default=get_current_timestamp
    )
    prov_password = Column(
        String, 
        nullable=False, 
        comment='Senha do fornecedor'
    )
    prov_hashed_password = Column(
        String, 
        nullable=False, 
        comment='Senha do fornecedor criptografada'
    )
    prov_token_str = Column(
        String, 
        nullable=False,
        comment='Token de acesso do fornecedor'
    )
    
class Companies(Base):
    """
    Empresas que usam o ERP.
    """
    __tablename__ = "companies"

    comp_id = Column(
        PrimaryKeyType, 
        primary_key=True, 
        index=True,
        comment='ID primário da empresa no banco'
    )
    comp_prov_id = Column(
        PrimaryKeyType, 
        index=True,
        comment='ID do ERP que a empresa usa'
    )
    comp_prco_id = Column(
        PrimaryKeyType, 
        primary_key=True, 
        index=True,
        comment='ID da empresa no ERP'
    )

class Product(Base):
    """
    Produtos vendidos pelas empresas.
    """
    __tablename__ = "products"

    prod_id = Column(PrimaryKeyType, primary_key=True, index=True)
    prod_prov_id = Column(PrimaryKeyType)
    prod_sku = Column(String, index=True)
    prod_name = Column(String)
    prod_description = Column(String)
    prod_category = Column(String, nullable = True)
    

class TransactionHistory(Base):
    """
    Transações realizadas pelas empresas.
    """
    __tablename__ = "transactions_history"

    trhi_id = Column(
        PrimaryKeyType, 
        primary_key=True, 
        nullable=False, 
        index=True
    )
    trhi_inserted_at = Column(DateTime, default=get_current_timestamp)
    trhi_processed_at = Column(DateTime)
    # Information provided by ERP
    trhi_tran_id = Column(
        Text, 
        nullable=False,
        comment='Número do Pedido ou NFe'
    )
    trhi_transated_at = Column(DateTime, nullable=False)
    trhi_prov_id = Column(
        Text, 
        nullable=False,
        comment='ID do fornecedor que enviou o arquivo'
    )
    trhi_comp_id = Column(
        Text, 
        nullable=False,
        comment='ID da empresa que enviou o arquivo'
    )
    trhi_salesperson_id = Column(
        Decimal,
        comment='ID do vendedor'
    )
    trhi_clie_id = Column(
        Text,
        comment='ID do Consumidor (CNPJ, CPF, COD)'
    )
    trhi_prod_sku = Column(
        Text, 
        nullable=False,
        comment='SKU do produto'
    )
    trhi_prod_sku_category = Column(
        Text,
        comment='Categoria do SKU do produto'
    )
    trhi_prod_price = Column(
        Decimal,
        default=0,
        comment='Preço do produto'
    )
    trhi_prod_quantity = Column(
        Decimal, 
        default=1,
        comment='Quantidade de produtos vendidos'
    )
    trhi_prod_order = Column(
        Integer, 
        default=0,
        comment='Ordem do produto no pedido'
    )
    trhi_freight_type = Column(
        Text, 
        default='',
        comment='Tipo de frete'
    )
    trhi_freight_value = Column(
        Decimal, 
        default=0,
        comment='Valor do frete'
    )
    trhi_commission = Column(
        Decimal, 
        default=0,
        comment='Comissão do vendedor'
    )
    trhi_remarks = Column(
        Text, 
        nullable=False, 
        default='',
        comment='Observações sobre o pedido ou item'
    )

class TransactionHistoryFile(Base):
    """ 
    Arquivos de histórico de transações enviados pelos fornecedores.
    """

    __tablename__ = "transactions_history_files"

    trhf_id = Column(PrimaryKeyType, primary_key=True, nullable=False, index=True)
    trhf_sent_at = Column(
        DateTime, 
        nullable=False,
        default=get_current_timestamp,
        comment='Data e hora do envio do arquivo'
    )
    trhf_processed_at = Column(
        Text, nullable=False,
        comment='Data e hora do processamento do arquivo'
    )
    trhf_prov_id = Column(
        Text, 
        nullable=False,
        comment='ID do fornecedor que enviou o arquivo'
    )
    trhf_comp_id = Column(
        Text, nullable=False,
        comment='ID da empresa que enviou o arquivo'
    )
    trhf_filename = Column(
        Text, nullable=False, 
        comment='Nome do arquivo armazenado, a ser processado. Este arquivo será enviado pelo ERP'
    )
    trhf_url = Column(
        Text, nullable=False,
        comment='URL do arquivo armazenado, a ser processado. Este arquivo será enviado pelo ERP'
    )
    trhf_status = Column(
        Text, nullable=False, comment='Não Processado | Processado | Erro'
    )
    trhf_size_kilobytes = Column(
        Decimal, nullable=False,
        comment='Tamanho do arquivo em kilobytes'
    )
    

class ProductPrediction(Base):
    """
    Recomendações e previsões de vendas de produtos.
    """

    __tablename__ = "product_predictions"

    pred_id = Column(PrimaryKeyType, primary_key=True, nullable=False, index=True)
    pred_prov_id = Column(
        Text, 
        nullable=False,
        comment='ID do fornecedor que enviou o arquivo'
    )
    pred_prco_id = Column(
        Text, 
        nullable=False,
        comment='ID do produto recomendado'
    )
    pred_clie_id = Column(
        Text,
        comment='ID do cliente que comprou o produto'
    )
    pred_prov_id = Column(Text)
    pred_prod_id = Column(Text, nullable=False)
    pred_hash_sku = Column(Text, nullable=False)
    pred_recommendation_json = Column(JSON, nullable=False)
    pred_recommendation_type = Column(Text, nullable=False)
    pred_recommendation_threshold = Column(Integer)
    
    # TODO: Implementar essas colunas
    # pred_forecast_quantity = Column(JSON)
    # pred_forecast_average_ticket = Column(JSON)
    # pred_forecast_next_purchase = Column(JSON)

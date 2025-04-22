# 📌 Visão Geral

Pipeline para coleta, processamento e armazenamento de dados de criptomoedas da API CoinCap, com armazenamento em PostgreSQL e estágios intermediários em JSON e Parquet.

## ✨ Funcionalidades

- Coleta dados de ativos e histórico da CoinCap API  
- Armazena dados brutos em JSON (`storage/raw/`)  
- Processa e armazena em Parquet (`storage/curated/`)  
- Carrega dados tratados no PostgreSQL 

## 🛠️ Tecnologias

- Python 3.11  
- PostgreSQL  
- Pandas - Processamento de dados  
- PyArrow - Formato Parquet  
- Psycopg2 - Conexão com PostgreSQL  
- Requests - Chamadas HTTP  

## ⚙️ Pré-requisitos

- Python 3.11  
- PostgreSQL 15+ instalado e rodando


## 🚀 Configuração Rápida

Clone o repositório:

```bash
git clone [URL_DO_REPOSITÓRIO]
cd crypto-data-pipeline
```

Crie e ative o ambiente virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🗂 Estrutura do Projeto

```
crypto-data-pipeline/
├── api/
│   └── coincap.py           # Cliente da API
├── database/
│   └── db_handler.py        # Manipulação do bando de dados
│   └── queries.sql          # Queries de criação das tabemas
├── storage/
│   ├── raw/                 # Dados brutos em JSON
│   └── curated/             # Dados processados em Parquet
├── utils/
│   ├── logger.py            # Configuração de logs
│   └── parquet_handler.py   # Manipulação de Parquet
│   └── storage_handler.py   # Manipulação de json
├── config.py                # Lê as variáveis de ambiente
├── main.py                  # Pipeline principal
├── .env.example             # Modelo de configuração
├── .env             		 # Arquivo de configuração utilizado
└── requirements.txt         # Dependências
```

## ▶️ Como Executar

Execute o pipeline completo:

```bash
python main.py
```

Ou módulos específicos:

```bash
# Apenas coleta
python -c "from api.coincap import CoinCapAPI; print(CoinCapAPI().get_assets())"

# Apenas processamento Parquet
python -c "from utils.parquet_handler import ParquetHandler; ParquetHandler().save_to_parquet(...)"
```

## 🔄 Fluxo de Dados

**Extração**: `api/coincap.py`  
- Coleta dados da API  
- Armazena JSON em `storage/raw/`  

**Transformação**: `utils/parquet_handler.py`  
- Converte para DataFrame  
- Armazena Parquet em `storage/curated/`  

**Carregamento**: `main.py`  
- Conecta ao PostgreSQL  
- Realiza upsert dos dados  

## 🛠️ Setup do Banco de Dados

Crie o banco de dados:

```sql
CREATE DATABASE postgres;
```

Execute o script SQL (encontrado em `database/queries.sql`):

```bash
psql -h localhost -U seu_usuario -d postgres -f database/queries.sql
```

## 📊 Modelo de Dados

```sql
-- Tabela de ativos
CREATE TABLE assets (
    id VARCHAR(50) PRIMARY KEY,
    rank INTEGER,
    symbol VARCHAR(10),
    name VARCHAR(100),
    supply NUMERIC,
    max_supply NUMERIC,
    market_cap_usd NUMERIC,
    volume_usd_24hr NUMERIC,
    price_usd NUMERIC,
    change_percent_24hr NUMERIC,
    vwap_24hr NUMERIC
);

-- Tabela de histórico
CREATE TABLE asset_history (
    id SERIAL PRIMARY KEY,
    asset_id VARCHAR(50) REFERENCES assets(id),
    date TIMESTAMP,
    price_usd NUMERIC
);
```
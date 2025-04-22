import pandas as pd
import os
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

logger = setup_logger()

class ParquetHandler:
    @staticmethod
    def get_project_root():
        """Retorna o caminho raiz do projeto de forma confiável"""
        return Path(__file__).parent.parent

    @staticmethod
    def get_parquet_path():
        """Retorna o caminho para armazenamento parquet relativo ao projeto"""
        project_root = ParquetHandler.get_project_root()
        return project_root / 'storage' / 'curated'

    @staticmethod
    def ensure_parquet_dir():
        """Garante que o diretório parquet existe"""
        try:
            parquet_path = ParquetHandler.get_parquet_path()
            parquet_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Parquet directory ensured: {parquet_path}")
        except Exception as e:
            logger.error(f"Error creating parquet directory: {str(e)}")
            raise

    @staticmethod
    def save_assets_to_parquet(data_type, assets_data):
        """Salva dados de ativos em arquivo parquet"""
        try:
            ParquetHandler.ensure_parquet_dir()
            parquet_path = ParquetHandler.get_parquet_path()
            
            df = pd.DataFrame(assets_data)
            
            # Seleção e renomeação de colunas
            df = df[['id', 'rank', 'symbol', 'name', 'supply', 'maxSupply', 
                    'marketCapUsd', 'volumeUsd24Hr', 'priceUsd', 
                    'changePercent24Hr', 'vwap24Hr']]
            
            df.columns = ['id', 'rank', 'symbol', 'name', 'supply', 'max_supply', 
                         'market_cap_usd', 'volume_usd_24hr', 'price_usd', 
                         'change_percent_24hr', 'vwap_24hr']
            
            # Conversão de tipos numéricos
            numeric_cols = ['supply', 'max_supply', 'market_cap_usd', 'volume_usd_24hr',
                          'price_usd', 'change_percent_24hr', 'vwap_24hr']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            
            # Caminho do arquivo
            # file_path = parquet_path / 'assets.parquet'
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.parquet"
            filepath = parquet_path / data_type / filename
            df.to_parquet(filepath, index=False)
            logger.info(f"Saved {len(df)} assets to {filepath}")
            
            return filepath
        
        except Exception as e:
            logger.error(f"Error saving assets to Parquet: {str(e)}")
            raise

    @staticmethod
    def save_history_to_parquet(asset_id, history_data, data_type, append=False):
        """Salva dados históricos em arquivo parquet"""

        ParquetHandler.ensure_parquet_dir()
        parquet_path = ParquetHandler.get_parquet_path()
        
        df = pd.DataFrame(history_data)
        
        df['asset_id'] = asset_id
        df['date'] = pd.to_datetime(df['time'], unit='ms')
        df['price_usd'] = pd.to_numeric(df['priceUsd'], errors='coerce')
        df = df[['asset_id', 'date', 'price_usd']]
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.parquet"
        filepath = parquet_path / data_type / filename
        if append and filepath.exists():
            existing_df = pd.read_parquet(filepath)
            df = pd.concat([existing_df, df]).drop_duplicates()
        
        df.to_parquet(filepath, index=False)
        logger.info(f"Saved {len(df)} history records to {filepath}")
        
        return filepath

    @staticmethod
    def read_parquet(file_name):
        """Lê um arquivo parquet da pasta padrão"""
        try:
            parquet_path = ParquetHandler.get_parquet_path()
            file_path = parquet_path / file_name
            df = pd.read_parquet(file_path)
            logger.info(f"lendo arquivo parquet do caminho {file_path}")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo parquet {file_name}: {str(e)}")
            raise
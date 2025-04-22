import psycopg2
from psycopg2 import sql, extras
from datetime import datetime
import pandas as pd
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger
from config import Config

logger = setup_logger()

class DBHandler:
    @staticmethod
    def get_connection():
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise

    @staticmethod
    def init_db():
        try:
            with open('database/queries.sql', 'r') as f:
                sql_commands = f.read()
            
            conn = DBHandler.get_connection()
            with conn.cursor() as cur:
                cur.execute(sql_commands)
            conn.commit()
            logger.info("Tabelas criadas com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao iniciar o banco de dados: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod            
    def get_project_root():
        """Retorna o caminho raiz do projeto de forma confiável"""
        return Path(__file__).parent.parent

    @staticmethod
    def get_curated_path():
        """Retorna o caminho para armazenamento raw relativo ao projeto"""
        project_root = DBHandler.get_project_root()
        curated_path = project_root / 'storage' / 'curated'
        return curated_path

    @staticmethod
    def insert_or_update_assets_from_parquet(data_type, filename):
        try:
            parquet_path = DBHandler.get_curated_path() / f'{data_type}/{filename}'
            logger.info(f"Lendo arquivo de assets de: {parquet_path}")
            
            df = pd.read_parquet(parquet_path)

            conn = DBHandler.get_connection()
            with conn.cursor() as cur:
                data = list(df.itertuples(index=False, name=None))

                query = """
                INSERT INTO assets (id, rank, symbol, name, supply, max_supply, 
                                  market_cap_usd, volume_usd_24hr, price_usd, 
                                  change_percent_24hr, vwap_24hr)
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                    rank = EXCLUDED.rank,
                    symbol = EXCLUDED.symbol,
                    name = EXCLUDED.name,
                    supply = EXCLUDED.supply,
                    max_supply = EXCLUDED.max_supply,
                    market_cap_usd = EXCLUDED.market_cap_usd,
                    volume_usd_24hr = EXCLUDED.volume_usd_24hr,
                    price_usd = EXCLUDED.price_usd,
                    change_percent_24hr = EXCLUDED.change_percent_24hr,
                    vwap_24hr = EXCLUDED.vwap_24hr
                """
                extras.execute_values(cur, query, data)
            
            conn.commit()
            logger.info(f"Dados inseridos/atualizados com sucesso: {len(df)} ativos")
        except Exception as e:
            logger.error(f"Erro ao processar assets do Parquet: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def insert_asset_history_from_parquet(data_type, filename):
        parquet_path = DBHandler.get_curated_path() / f'{data_type}/{filename}'
        logger.info(f"Lendo arquivo de histórico de: {parquet_path}")
        
        df = pd.read_parquet(parquet_path)
        
        conn = DBHandler.get_connection()
        with conn.cursor() as cur:
            data = list(df.itertuples(index=False, name=None))
            
            query = """
            INSERT INTO asset_history (asset_id, date, price_usd)
            VALUES %s
            """
            extras.execute_values(cur, query, data)
        
        conn.commit()
        logger.info(f"Dados históricos inseridos/atualizados: {len(df)} registros")
        conn.close()

    @staticmethod
    def get_last_update_date(asset_id=None):
        """Obtém a data do último update no banco de dados"""
        try:
            conn = DBHandler.get_connection()
            with conn.cursor() as cur:
                if asset_id:
                    query = """
                    SELECT MAX(date) FROM asset_history WHERE asset_id = %s
                    """
                    cur.execute(query, (asset_id,))
                else:
                    query = "SELECT MAX(date) FROM asset_history"
                    cur.execute(query)
                
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao obter última data de update: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
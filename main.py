from api.coincap import CoinCapAPI
from database.db_handler import DBHandler
from utils.parquet_handler import ParquetHandler
from utils.storage_handler import StorageHandler
import time
import sys
import os
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

logger = setup_logger()


def main():
    DBHandler.init_db()
    
    api = CoinCapAPI()
    
    try:
        logger.info("Fetching assets data...")
        assets_response = api.get_assets()
        assets = assets_response.get('data', [])

        StorageHandler.save_raw_json('assets', assets)
        ParquetHandler.save_assets_to_parquet('assets', assets)
        
        filename = os.listdir(f"{Path(__file__).parent}\\storage\\curated\\assets")
        filename = filename[0] #limita para um arquivo json
        DBHandler.insert_or_update_assets_from_parquet('assets', filename)
        
        for asset in assets[0:10]: #limita as chamadas de api para dados historios
            logger.info(f"Fetching historical data for {asset['id']}...")
            history_response = api.get_asset_history(asset['id'], interval="d1")
            history_data = history_response.get('data', [])

            if history_data:

                StorageHandler.save_raw_json('assets_history', history_data)
                ParquetHandler.save_history_to_parquet(asset['id'], history_data, 'assets_history')
                time.sleep(1)


        filenames = os.listdir(f"{Path(__file__).parent}\\storage\\curated\\assets_history")
        for filename in filenames:
            DBHandler.insert_asset_history_from_parquet('assets_history',filename)
            
    except Exception as e:
        logger.error(f"Fatal error in main process: {str(e)}")
        raise


if __name__ == "__main__":
    main()
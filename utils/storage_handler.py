import os
import json
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

logger = setup_logger()

class StorageHandler:
    @staticmethod
    def get_project_root():
        """Retorna o caminho raiz do projeto de forma confiável"""
        return Path(__file__).parent.parent

    @staticmethod
    def get_raw_storage_path():
        """Retorna o caminho para armazenamento raw relativo ao projeto"""
        project_root = StorageHandler.get_project_root()
        raw_path = project_root / 'storage' / 'raw'
        return raw_path

    @staticmethod
    def ensure_directory(path):
        """Cria o diretório se não existir"""
        try:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {path}")
        except OSError as e:
            logger.error(f"Error creating directory {path}: {str(e)}")
            raise

    @staticmethod
    def save_raw_json(data_type, data, subfolder=None):
        """
        Salva dados brutos em JSON na estrutura:
        <project_root>/storage/raw/<data_type>/[subfolder]/<timestamp>.json
        """
        try:
            base_path = StorageHandler.get_raw_storage_path()
            if subfolder:
                save_path = base_path / data_type / subfolder
            else:
                save_path = base_path / data_type
    
            StorageHandler.ensure_directory(save_path)
            
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.json"
            filepath = save_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved raw {data_type} data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving raw {data_type} data: {str(e)}")
            raise
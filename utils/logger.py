import logging
import sys

def setup_logger():
    logger = logging.getLogger('crypto_data_collector')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    fh = logging.FileHandler('crypto_data_collector.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger
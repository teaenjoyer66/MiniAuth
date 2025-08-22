import json
import logging 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DATA_DIR = ROOT_DIR / 'data'
CACHE_FILEPATH = DATA_DIR / "offline_cache.json"

def save_offline_cache(json_data: dict, cache_path: Path = CACHE_FILEPATH) -> None:    
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
            
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        logging.info(f"Offline cache saved to {cache_path}")
    
    except Exception as e:
        logging.error(f"Failed to save offline cache: {e}")
        
def load_offline_cache(cache_path: Path = CACHE_FILEPATH):
    try:
        if not cache_path.exists():
            logging.warning(f"Cache file {cache_path} does not exist.")
            return None
        
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        logging.info(f"Offline cache loaded from {cache_path}")
        return data
    
    except Exception as e:
        logging.error(f"Failed to load offline cache: {e}")
        return None
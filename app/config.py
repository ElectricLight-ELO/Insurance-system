from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "osago.db"
STORAGE_DIR = DATA_DIR / "storage"
STATIC_DIR = BASE_DIR / "static"

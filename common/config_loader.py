import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
GLOBAL_CONFIG_PATH = BASE_DIR / "global_config.yaml"

def load_global_config() -> dict:
    with open(GLOBAL_CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

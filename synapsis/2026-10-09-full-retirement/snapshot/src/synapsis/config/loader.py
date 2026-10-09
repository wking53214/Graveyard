import yaml
from pathlib import Path

CONFIG_ROOT = Path.home() / "synapsis" / "config"

def load_config(name: str) -> dict:
    path = CONFIG_ROOT / f"{name}.yaml"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

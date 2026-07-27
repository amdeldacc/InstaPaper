import toml
from pathlib import Path

CONFIG_PATH = Path.home() / ".instapaper" / "config.toml"

def load() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return toml.loads(CONFIG_PATH.read_text())

def save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(toml.dumps(data))
    CONFIG_PATH.chmod(0o600)

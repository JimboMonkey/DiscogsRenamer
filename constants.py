import tomllib
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

APP_NAME = "DiscogsRenamer"
PACKAGE_NAME = "discogsrenamer"

try:
    APP_VERSION = version(PACKAGE_NAME)
except PackageNotFoundError:
    data = tomllib.loads(Path("pyproject.toml").read_text())
    APP_VERSION = data["project"]["version"]

"""rules-system-bound: Living Container Framework."""

from importlib.metadata import PackageNotFoundError, version

from .config import Config, get_config
from .container import Container, ContainmentRules
from .idealization import (
    IdealizationType,
    IdealizedForm,
    IdealizationManager,
    co_constitute,
    reflect,
    refract,
    project,
    approximate,
)
from .interaction import Interaction, System, InteractionEmergence

try:
    __version__ = version("rules-system-bound")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "Config",
    "get_config",
    "Container",
    "ContainmentRules",
    "IdealizationType",
    "IdealizedForm",
    "IdealizationManager",
    "Interaction",
    "System",
    "InteractionEmergence",
    "co_constitute",
    "reflect",
    "refract",
    "project",
    "approximate",
]

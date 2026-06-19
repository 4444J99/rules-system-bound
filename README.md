# rules-system-bound

A generalized system for organizing hierarchically nested containers where the hierarchy emerges from the contained systems themselves, not predetermined levels.

## Overview

The Living Container Framework provides rules for:

- **Containment**: Multi-factor rules (function + scale + boundary) with context-dependent precedence
- **Idealized Forms**: Co-constitutive relationship between Platonic, Weberian, and Normalized forms
- **Interaction Emergence**: Interactions emerge from what systems ARE, not predefined categories
- **Self-Defining Boundaries**: Top boundary defined by the boundary question itself

## Installation

```bash
git clone https://github.com/organvm-i-theoria/rules-system-bound.git
cd rules-system-bound
python3 -m pip install -e ".[dev]"
```

The package also installs a console script:

```bash
rules-system-bound --json
```

## Quick Start

```python
from rules_system_bound import Container, ContainmentRules, System, InteractionEmergence

# Create containers
universe = Container(id="universe", function="all", purpose="contains everything")
system = Container(id="system", function="organized", purpose="organized function")

# Create containment rules
rules = ContainmentRules()

# Check if universe can contain system
can_contain = universe.can_contain(system, rules)

# Create systems and discover interactions
s1 = System(id="s1", function="process", purpose="does work", scale=1.0)
s2 = System(id="s2", function="store", purpose="holds data", scale=1.0)

emergence = InteractionEmergence()
emergence.register_system(s1)
emergence.register_system(s2)

interactions = emergence.discover_interactions(s1, s2)
```

## Runnable Evidence

From a checkout, the activation smoke path is:

```bash
PYTHONPATH=src python3 -m rules_system_bound --json
```

After installation, the release path is:

```bash
rules-system-bound --json
```

See [docs/activation-audit.md](docs/activation-audit.md) for the audit receipt
and the exact install/test commands.

## Core Concepts

### Container Contract

Every container defines:
- **FUNCTION**: What it enables/produces
- **PURPOSE**: Why it exists
- **LIMITS**: What it cannot do
- **BOUNDARY**: Permeability type (porous, semi_permeable, sealed)

### Containment Rules

Multi-factor containment:
1. Function compatibility
2. Scale relation
3. Boundary permeability

### Idealized Forms

Three types that co-constitute with real systems:
- **PLATONIC**: Perfect archetype
- **WEBERIAN**: Essential function captured
- **NORMALIZED**: Representation of real instances

## Runnable Evidence

From a checkout, the activation smoke path is:

```bash
PYTHONPATH=src python3 -m rules_system_bound --json
```

After installation, the release path is:

```bash
rules-system-bound --json
```

See [docs/activation-audit.md](docs/activation-audit.md) for the audit receipt
and the exact install/test commands.

## Configuration

Copy `.env.template` to `.env` and customize:

```bash
cp .env.template .env
```

## Development

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev]"

# Run tests
pytest tests -v

# Run activation smoke path
rules-system-bound --json

# Lint
ruff check src tests
```

## Structure

```
src/rules_system_bound/
├── __init__.py
├── config.py       # Configuration loader
├── container.py   # Container model & containment rules
├── idealization.py # Idealized forms
└── interaction.py # Interaction emergence
```

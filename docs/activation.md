# Activation Evidence

Issue: `organvm-i-theoria/rules-system-bound#2`
Audit cursor: `EV-2026-06-11-200204`
Audit date: 2026-06-11
Remediation date: 2026-06-18

## Identity

`rules-system-bound` is a Python package for a hierarchical rule/container
constraint system. It models containment boundaries, emergent interactions, and
idealized forms for theory-layer systems.

## Runtime Surface

This repository ships a library package plus a small executable activation check.
It is not a hosted web service, so there is no live URL to document.

Install from a checkout:

```bash
git clone https://github.com/organvm-i-theoria/rules-system-bound.git
cd rules-system-bound
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
```

Run directly from an uninstalled repository checkout:

```bash
PYTHONPATH=src python3 -m rules_system_bound --json
```

Run after package installation:

```bash
rules-system-bound --json
```

Expected activation result:

```json
{
  "package": "rules-system-bound",
  "status": "ok"
}
```

The full JSON output also includes containment and interaction smoke-check
details.

## Verification

```bash
python3 -m pytest -q
PYTHONPATH=src python3 -m rules_system_bound --json
```

CI is declared at `.github/workflows/ci-python.yml` and runs install, tests,
lint, and the activation command.

## Audit Resolution

- Live URL: not applicable; package/CLI repo, no hosted service.
- Installable package: documented via `python3 -m pip install -e ".[dev]"`.
- Runnable release path: documented via
  `PYTHONPATH=src python3 -m rules_system_bound --json` and installed
  `rules-system-bound --json`.
- Documented exec path: README and this activation evidence file.
- Evidence level after remediation: runnable-from-repo plus installable package.

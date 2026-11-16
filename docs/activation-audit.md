# Activation Audit Evidence

Issue: `organvm-i-theoria/rules-system-bound#2`
Cursor: `EV-2026-06-11-200204`

## Shipping Surface

- Identity: hierarchical rule/container constraint system.
- Package: `rules-system-bound` Python library.
- Live URL: not applicable; this repository ships a Python library and CLI, not a hosted web service.
- Installable package path: `python3 -m pip install git+https://github.com/organvm-i-theoria/rules-system-bound.git`.
- Editable install path: `python3 -m pip install -e ".[dev]"`.
- Runnable release path after install: `rules-system-bound --json`.
- Runnable path from checkout: `PYTHONPATH=src python3 -m rules_system_bound --json`.
- Test path from checkout: `PYTHONPATH=src python3 -m pytest -q`.

## Evidence Command

Run the activation smoke path from a fresh checkout:

```bash
git clone https://github.com/organvm-i-theoria/rules-system-bound.git
cd rules-system-bound
PYTHONPATH=src python3 -m rules_system_bound --json
```

The command exercises the public package API by constructing a container,
checking containment rules, discovering interactions, and creating a
co-constitutive idealization relation. A successful run emits JSON with
`"status": "runnable"`.

After package installation, use the console script:

```bash
python3 -m pip install -e ".[dev]"
rules-system-bound --json
python3 -m pytest -q
```

## Activation Result

The repository now has a documented execution path and an install-time console
script. The remaining external release step, if needed, is publishing a tagged
artifact to a package registry; no registry credentials or hosted endpoint are
required for the current library surface.

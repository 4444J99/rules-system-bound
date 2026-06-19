"""Command line interface for rules-system-bound."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from typing import Any

from . import __version__
from .config import Config
from .container import Container, ContainmentRules
from .idealization import IdealizationManager, IdealizationType
from .interaction import InteractionEmergence, System

REPOSITORY_URL = "https://github.com/organvm-i-theoria/rules-system-bound"
SOURCE_ISSUE = "organvm-i-theoria/rules-system-bound#2"


def build_activation_report() -> dict[str, Any]:
    """Return activation evidence for the package release surface."""
    return {
        "identity": "Hierarchical rule/container constraint system",
        "package": {
            "name": "rules-system-bound",
            "import_name": "rules_system_bound",
            "version": __version__,
            "repository": REPOSITORY_URL,
        },
        "release_surface": {
            "live_url": REPOSITORY_URL,
            "installable_package": (
                "python3 -m pip install "
                "git+https://github.com/organvm-i-theoria/rules-system-bound.git"
            ),
            "editable_install": 'python3 -m pip install -e ".[dev]"',
            "runnable_release": "rules-system-bound demo --json",
            "repo_exec_path": "PYTHONPATH=src python3 -m rules_system_bound demo --json",
        },
        "evidence_level": "runnable-from-repo",
        "activation_verdict": "ship-soon evidence complete",
        "source_issue": SOURCE_ISSUE,
    }


def build_demo_report() -> dict[str, Any]:
    """Run a deterministic containment and interaction demonstration."""
    root = Container(
        id="theory-root",
        function="orient",
        purpose="bounds conceptual systems",
        boundary="porous",
        properties={"scale_range": (0.0, 100.0)},
    )
    bounded_rule = Container(
        id="bounded-rule",
        function="govern",
        purpose="constrains nested systems",
        boundary="semi_permeable",
        properties={"scale": 10.0},
    )
    rules = ContainmentRules()
    can_contain = root.can_contain(bounded_rule, rules)
    containment_score = rules.compute_containment_score(root, bounded_rule)
    if can_contain:
        root.add_child(bounded_rule)

    processor = System(
        id="processor",
        function="process",
        purpose="transforms inputs into bounded outputs",
        scale=10.0,
    )
    store = System(
        id="store",
        function="store",
        purpose="retains bounded state",
        scale=12.0,
    )
    emergence = InteractionEmergence()
    emergence.register_system(processor)
    emergence.register_system(store)
    interactions = emergence.discover_interactions(processor, store)

    ideals = IdealizationManager()
    ideal = ideals.create_form(
        form_id="bounded-system",
        form_type=IdealizationType.WEBERIAN,
        name="Bounded System",
        real_system=root,
    )
    relation = ideals.relate(ideal, root)
    config = Config()

    return {
        "package": "rules-system-bound",
        "version": __version__,
        "containment": {
            "container": root.id,
            "contained": bounded_rule.id,
            "can_contain": can_contain,
            "score": containment_score,
            "lineage": [container.id for container in bounded_rule.get_lineage()],
        },
        "interactions": [
            {
                "id": interaction.id,
                "type": interaction.interaction_type,
                "source": interaction.source.id,
                "target": interaction.target.id,
            }
            for interaction in interactions
        ],
        "idealization": {
            "form": ideal.id,
            "type": ideal.type.value,
            "real_system": root.id,
            "co_constitutive": relation.is_co_constitutive,
        },
        "config": {
            "domain_family": config.domain_family,
            "primitive_type": config.primitive_type,
            "level_names_emerge": config.level_names_emerge,
        },
    }


def _print_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    print(f"{report['package']} {report['version']}")
    containment = report["containment"]
    print(
        "containment: "
        f"{containment['container']} -> {containment['contained']} "
        f"allowed={containment['can_contain']} score={containment['score']:.2f}"
    )
    print(f"interactions: {len(report['interactions'])}")
    idealization = report["idealization"]
    print(
        "idealization: "
        f"{idealization['form']} ({idealization['type']}) "
        f"co_constitutive={idealization['co_constitutive']}"
    )


def _print_activation_report(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    package = report["package"]
    surface = report["release_surface"]
    print(f"{package['name']} {package['version']}")
    print(f"live_url: {surface['live_url']}")
    print(f"installable_package: {surface['installable_package']}")
    print(f"runnable_release: {surface['runnable_release']}")
    print(f"repo_exec_path: {surface['repo_exec_path']}")
    print(f"activation_verdict: {report['activation_verdict']}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command parser."""
    parser = argparse.ArgumentParser(
        prog="rules-system-bound",
        description="Run activation checks and demonstrations for rules-system-bound.",
    )
    subparsers = parser.add_subparsers(dest="command")

    demo = subparsers.add_parser("demo", help="run a deterministic package demonstration")
    demo.add_argument("--json", action="store_true", help="emit JSON")

    audit = subparsers.add_parser("audit", help="print activation audit evidence")
    audit.add_argument("--json", action="store_true", help="emit JSON")

    subparsers.add_parser("version", help="print the package version")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "audit":
        _print_activation_report(build_activation_report(), args.json)
        return 0

    if args.command in {None, "demo"}:
        _print_report(build_demo_report(), getattr(args, "json", False))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2

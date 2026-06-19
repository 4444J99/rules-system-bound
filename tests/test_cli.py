"""Tests for the activation command line interface."""

import json

from rules_system_bound.cli import build_activation_report, build_demo_report, main


def test_activation_report_documents_release_surface():
    """Activation report names the documented live and runnable surfaces."""
    report = build_activation_report()

    assert report["release_surface"]["live_url"].endswith("/rules-system-bound")
    assert "pip install" in report["release_surface"]["installable_package"]
    assert report["release_surface"]["runnable_release"] == "rules-system-bound demo --json"
    assert report["release_surface"]["repo_exec_path"].startswith("PYTHONPATH=src")
    assert report["source_issue"] == "organvm-i-theoria/rules-system-bound#2"


def test_demo_report_exercises_core_package():
    """Demo report runs containment, interaction, and idealization paths."""
    report = build_demo_report()

    assert report["containment"]["can_contain"] is True
    assert report["containment"]["score"] == 1.0
    assert report["containment"]["lineage"] == ["bounded-rule", "theory-root"]
    assert {interaction["type"] for interaction in report["interactions"]} == {
        "boundary_exchange",
        "function_coupling",
        "scale_resonance",
    }
    assert report["idealization"]["co_constitutive"] is True


def test_cli_audit_json_output(capsys):
    """CLI emits machine-readable audit evidence."""
    exit_code = main(["audit", "--json"])

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["activation_verdict"] == "ship-soon evidence complete"


def test_cli_demo_is_default(capsys):
    """The package is runnable with no subcommand."""
    exit_code = main([])

    assert exit_code == 0
    assert "containment:" in capsys.readouterr().out

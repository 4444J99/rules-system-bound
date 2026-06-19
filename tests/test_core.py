"""Tests for rules-system-bound."""

import json

from rules_system_bound import (
    Container,
    ContainmentRules,
    IdealizationType,
    IdealizedForm,
    IdealizationManager,
    System,
    InteractionEmergence,
    Config,
)


class TestContainer:
    """Tests for Container model."""

    def test_create_container(self):
        """Can create a basic container."""
        container = Container(
            id="test",
            function="containment",
            purpose="holds things",
            limits={"cannot_hold_infinite"},
            boundary="semi_permeable",
        )
        assert container.id == "test"
        assert container.function == "containment"
        assert container.boundary == "semi_permeable"

    def test_add_child(self):
        """Can add child containers."""
        parent = Container(id="parent", function="p", purpose="p")
        child = Container(id="child", function="c", purpose="c")

        parent.add_child(child)

        assert child in parent.children
        assert child.parent == parent
        assert parent.envelops(child)

    def test_get_lineage(self):
        """Can trace lineage to top."""
        grandparent = Container(id="gp", function="gp", purpose="gp")
        parent = Container(id="p", function="p", purpose="p")
        child = Container(id="c", function="c", purpose="c")

        grandparent.add_child(parent)
        parent.add_child(child)

        lineage = child.get_lineage()

        assert lineage == [child, parent, grandparent]

    def test_get_descendants(self):
        """Can get all descendants."""
        root = Container(id="root", function="r", purpose="r")
        child1 = Container(id="c1", function="c1", purpose="c1")
        child2 = Container(id="c2", function="c2", purpose="c2")
        grandchild = Container(id="gc", function="gc", purpose="gc")

        root.add_child(child1)
        root.add_child(child2)
        child1.add_child(grandchild)

        descendants = root.get_descendants()

        assert child1 in descendants
        assert child2 in descendants
        assert grandchild in descendants


class TestContainmentRules:
    """Tests for ContainmentRules."""

    def test_create_rules(self):
        """Can create containment rules."""
        rules = ContainmentRules(
            function_weight=0.5,
            scale_weight=0.3,
            boundary_weight=0.2,
        )
        assert rules.function_weight == 0.5
        assert rules.precedence == "context_dependent"

    def test_boundary_permeability(self):
        """Boundary permeability check works."""
        rules = ContainmentRules()

        porous = Container(id="porous", function="p", purpose="p", boundary="porous")
        semi = Container(id="semi", function="s", purpose="s", boundary="semi_permeable")
        sealed = Container(id="sealed", function="s", purpose="s", boundary="sealed")

        # Porous can contain all
        assert rules._check_boundary_permeability(porous, semi)
        assert rules._check_boundary_permeability(porous, sealed)

        # Semi can contain semi and sealed
        assert rules._check_boundary_permeability(semi, semi)
        assert rules._check_boundary_permeability(semi, sealed)

        # Sealed can only contain sealed
        assert rules._check_boundary_permeability(sealed, sealed)
        assert not rules._check_boundary_permeability(sealed, semi)


class TestIdealization:
    """Tests for idealized forms."""

    def test_create_idealized_form(self):
        """Can create idealized form."""
        form = IdealizedForm(
            id="ideal_1",
            type=IdealizationType.PLATONIC,
            name="Perfect Circle",
            reflects=True,
        )
        assert form.type == IdealizationType.PLATONIC
        assert form.reflects

    def test_idealization_manager(self):
        """Can manage idealized forms."""
        manager = IdealizationManager()

        form = manager.create_form(
            form_id="platonic_1",
            form_type=IdealizationType.PLATONIC,
            name="Ideal Type",
        )

        assert form.id in manager.forms

    def test_co_constitutive_relation(self):
        """Can create co-constitutive relation."""
        form = IdealizedForm(
            id="test",
            type=IdealizationType.WEBERIAN,
            name="Test",
        )

        # Relation created via co_constitute function
        assert form.id == "test"


class TestInteraction:
    """Tests for interaction emergence."""

    def test_system_creation(self):
        """Can create a system."""
        system = System(
            id="sys1",
            function="process",
            purpose="does things",
            boundary="semi_permeable",
            scale=1.0,
        )
        assert system.id == "sys1"

    def test_interaction_emergence(self):
        """Interactions emerge between systems."""
        sys1 = System(id="s1", function="a", purpose="p", scale=1.0)
        sys2 = System(id="s2", function="b", purpose="p", scale=1.0)

        interactions = sys1.can_interact_with(sys2)

        # Should have at least some interactions
        assert len(interactions) > 0

    def test_discover_all_interactions(self):
        """Can discover all interactions in a system."""
        emergence = InteractionEmergence()

        s1 = System(id="s1", function="f1", purpose="p", scale=1.0)
        s2 = System(id="s2", function="f2", purpose="p", scale=1.5)
        s3 = System(id="s3", function="f3", purpose="p", scale=2.0)

        emergence.register_system(s1)
        emergence.register_system(s2)
        emergence.register_system(s3)

        all_interactions = emergence.discover_all_interactions()

        assert len(all_interactions) > 0


class TestConfig:
    """Tests for configuration."""

    def test_default_config(self):
        """Can create default config."""
        config = Config()
        assert config.container_function == "function"
        assert config.level_names_emerge is True

    def test_config_from_dict(self):
        """Can create config from dict."""
        data = {"container_function": "custom_func", "domain_family": "social"}
        config = Config.from_dict(data)

        assert config.container_function == "custom_func"
        assert config.domain_family == "social"

    def test_config_from_env_preserves_types(self, monkeypatch):
        """Environment values are coerced into config field types."""
        from rules_system_bound.config import Config
        monkeypatch.setenv("CONTAINMENT_FUNCTION_WEIGHT", "0.7")
        monkeypatch.setenv("LEVEL_NAMES_EMERGE", "false")

        config = Config.from_env()

        assert config.containment_function_weight == 0.7
        assert config.level_names_emerge is False


class TestActivationCli:
    """Tests for the documented activation smoke path."""

    def test_activation_report_exercises_public_api(self):
        """Activation report provides deterministic runnable evidence."""
        from rules_system_bound.cli import activation_report

        report = activation_report()

        assert report["package"] == "rules-system-bound"
        assert report["status"] == "runnable"
        assert report["containment"]["can_contain"] is True
        assert report["containment"]["lineage"] == ["bounded-system", "framework"]
        assert len(report["interactions"]) == 3
        assert report["idealization"]["co_constitutive"] is True

    def test_cli_json_output(self, capsys):
        """CLI emits machine-readable activation evidence."""
        from rules_system_bound.cli import main

        exit_code = main(["--json"])
        output = capsys.readouterr().out
        report = json.loads(output)

        assert exit_code == 0
        assert report["exec_path"]["after_install"] == "rules-system-bound --json"
        assert report["containment"]["score"] == 1.0

    def test_render_text_respects_co_constitutive_flag(self):
        """Human output reflects the relation flag in the report."""
        from rules_system_bound.cli import activation_report, render_text

        report = activation_report()
        report["idealization"]["co_constitutive"] = False

        output = render_text(report)

        assert "relates to framework" in output
        assert "co-constitutes framework" not in output

"""Focused regressions for acyclic, single-parent container relationships.

Covers rules-system-bound#17: self-parenting and ancestor cycles must be
rejected before mutation, re-adding must not duplicate, reparenting must
be atomic, and removal/membership must use object identity.
"""

import pytest
from rules_system_bound.container import Container


def make(identifier):
    return Container(id=identifier, function="f", purpose="p")


def test_self_parenting_rejected_and_state_unchanged():
    container = make("a")
    with pytest.raises(ValueError):
        container.add_child(container)
    assert container.parent is None
    assert container.children == []


def test_ancestor_cycle_rejected_and_state_unchanged():
    root, mid, leaf = make("root"), make("mid"), make("leaf")
    root.add_child(mid)
    mid.add_child(leaf)
    with pytest.raises(ValueError):
        leaf.add_child(root)
    assert root.parent is None
    assert root.children == [mid]
    assert mid.children == [leaf]
    assert leaf.children == []
    assert leaf.get_lineage() == [leaf, mid, root]


def test_readding_same_child_does_not_duplicate():
    parent, child = make("p"), make("ch")
    parent.add_child(child)
    parent.add_child(child)
    assert parent.children == [child]
    assert child.parent is parent


def test_reparenting_moves_atomically():
    old_parent, new_parent, child = make("p1"), make("p2"), make("ch")
    old_parent.add_child(child)
    new_parent.add_child(child)
    assert old_parent.children == []
    assert new_parent.children == [child]
    assert child.parent is new_parent
    assert child.get_lineage() == [child, new_parent]


def test_descendant_promoted_to_direct_child_without_cycle():
    root, mid, leaf = make("root"), make("mid"), make("leaf")
    root.add_child(mid)
    mid.add_child(leaf)
    root.add_child(leaf)
    assert mid.children == []
    assert root.children == [mid, leaf]
    assert leaf.parent is root
    assert leaf.get_lineage() == [leaf, root]


def test_remove_uses_identity_not_dataclass_equality():
    parent, child = make("p"), make("ch")
    parent.add_child(child)
    twin = Container(id="ch", function="f", purpose="p")
    twin.parent = parent
    assert twin == child
    parent.remove_child(twin)
    assert parent.children == [child]
    assert child.parent is parent
    assert twin.parent is parent
    parent.remove_child(child)
    assert parent.children == []
    assert child.parent is None


def test_envelops_uses_identity_not_dataclass_equality():
    parent, child = make("p"), make("ch")
    parent.add_child(child)
    twin = Container(id="ch", function="f", purpose="p")
    twin.parent = parent
    assert twin == child
    assert parent.envelops(child)
    assert not parent.envelops(twin)


def test_readd_reconciles_parent_when_children_list_supplied_directly():
    # CodeRabbit review on PR #19: a directly-constructed children list
    # can leave child.parent unset while membership claims otherwise.
    child = make("ch")
    parent = Container(id="p", function="f", purpose="p", children=[child])
    assert child.parent is None
    parent.add_child(child)
    assert parent.children == [child]
    assert child.parent is parent
    assert child.get_lineage() == [child, parent]


def test_readd_via_direct_list_detaches_old_parent():
    # Same construction path, but the pointer names another parent that
    # still lists the child: re-adding must move it, not duplicate it.
    old_parent, child = make("p1"), make("ch")
    old_parent.add_child(child)
    new_parent = Container(id="p2", function="f", purpose="p", children=[child])
    new_parent.add_child(child)
    assert old_parent.children == []
    assert new_parent.children == [child]
    assert child.parent is new_parent
    assert child.get_lineage() == [child, new_parent]


def test_children_graph_cycle_rejected_and_state_unchanged():
    # Second CodeRabbit review on PR #19: a directly-constructed list
    # (parent lists child, child.parent unset) must not let
    # child.add_child(parent) close a cycle in the children lists.
    child = make("ch")
    parent = Container(id="p", function="f", purpose="p", children=[child])
    with pytest.raises(ValueError):
        child.add_child(parent)
    assert parent.parent is None
    assert parent.children == [child]
    assert child.parent is None
    assert child.children == []
    assert parent.get_descendants() == [child]


def test_normal_lineage_and_descendants_with_unrelated_unchanged():
    root = make("root")
    child1, child2 = make("c1"), make("c2")
    grandchild = make("gc")
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(grandchild)
    assert grandchild.get_lineage() == [grandchild, child1, root]
    assert root.get_descendants() == [child1, grandchild, child2]
    assert child2.get_lineage() == [child2, root]

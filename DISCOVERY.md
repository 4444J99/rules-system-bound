# Discovery: organvm/rules-system-bound

**Verdict: PROMOTE — real value, build-out warranted.**

`rules-system-bound` is a working Python library that formalizes hierarchical containment as a programmable, semantically-typed data model: `Container` (function, purpose, limits, boundary permeability), `ContainmentRules` (weighted multi-factor scoring across function compatibility, scale, and boundary), `IdealizationManager` (Platonic/Weberian/Normalized idealized-form types with co-constitutive relations), and `InteractionEmergence` (emergent interaction discovery between systems). All four modules are installable from PyPI or source, CI-green, and exercise a documented CLI (`rules-system-bound --json`). The highest latent value is as the **ontological substrate for the organvm estate itself**: the estate's 145 repos and 10 organs are precisely the hierarchically-nested containers this library models — each possessing a function, purpose, boundary permeability (porous open-source vs. sealed private), and scale. Wiring `ContainmentRules.compute_containment_score()` to the estate's actual governance rules would yield a machine-queryable, composable placement engine — replacing manual CLAUDE.md-based organ categorization with computed containment decisions that can route new repos automatically. The library's current weakness is that `_check_function_compatibility()` is a placeholder (always returns `True`), which means the weighted scoring is not yet meaningful; fixing this is the single best first task: implement keyword-overlap or embedding-based semantic similarity between `function` strings (~50 lines) to make `compute_containment_score()` return real values and unlock the library's core discriminating power.

**Single best first task:** Implement `ContainmentRules._check_function_compatibility()` with a real semantic check (e.g., Jaccard similarity over `function` string tokens) so the weighted containment score in `compute_containment_score()` reflects actual functional affinity rather than always returning `1.0`.

---

*Discovered: 2026-06-23 | Discoverer: limen/discover-organvm-rules-system-bound-ce4c*

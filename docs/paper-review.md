# Paper Review

This page is a professional review board for public designs that can become
future layout reproduction, simulation, analysis, and circuit-model targets.

Only public information belongs here. Do not copy private lab notes, private
layout parameters, or unpublished run evidence into these entries.

Each review item should eventually include:

- public citation or DOI;
- design family and geometry class;
- what can be reproduced as public layout;
- simulation targets;
- circuit-model targets;
- material/layer assumptions;
- publication-safe validation evidence.

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card} PAPER-001 CPW resonator references
:link: papers/cpw-resonator-references
:link-type: doc

**Design family:** resonator

**Status:** source selection

Collect public resonator papers suitable for reproducing a clean CPW layout,
Palace electrostatic/EPR setup, benchmark record, and reduced circuit model.
:::

:::{grid-item-card} PAPER-002 Transmon reference designs
:link: papers/transmon-reference-designs
:link-type: doc

**Design family:** qubit

**Status:** source selection

Collect public transmon or related qubit papers where geometry, materials, and
analysis assumptions are clear enough for a public reproduction workflow.
:::

:::{grid-item-card} PAPER-003 Flip-chip and 3D integration
:link: papers/flip-chip-3d-integration
:link-type: doc

**Design family:** multi-die / package

**Status:** source selection

Collect public flip-chip or 3D superconducting circuit papers that can exercise
multi-face layer semantics, indium bump assumptions, and package-scale
simulation workflows.
:::

:::{grid-item-card} PAPER-004 Surface loss and participation studies
:link: papers/surface-loss-participation
:link-type: doc

**Design family:** analysis method

**Status:** source selection

Collect public studies that define useful targets for surface participation,
surface-Q mapping, dielectric loss attribution, and report validation.
:::

::::

```{toctree}
:hidden:

papers/cpw-resonator-references
papers/transmon-reference-designs
papers/flip-chip-3d-integration
papers/surface-loss-participation
```

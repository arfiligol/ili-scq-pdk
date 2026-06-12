# Home

`ili-scq-pdk` is the public superconducting quantum/RF PDK for contributors who
need to keep a Primary Layout in a private repository while still improving
shared GDSFactory ecosystem infrastructure.

The public PDK does not migrate private layout/IP into a public repo. It owns
the public process contract: layer names, layer views, the layer stack, material
semantics, public demo cells, provider discovery, and publication-safe
documentation. Private layout repositories keep real chip geometry, private
parameters, private notebooks, GDS inputs from private designs, and private
run evidence.

The intended workflow is local and reviewable: install the public PDK,
ecosystem forks, and an optional private layout provider into the same Python
environment; use private layouts to validate public infrastructure; then slice
accepted public work into clean upstream PR branches.

## Start By Task

::::{grid} 1 1 2 3
:gutter: 3

:::{grid-item-card} Use The Public PDK
:link: home/pdk-responsibilities
:link-type: doc

Understand what `ili-scq-pdk` owns: public process semantics, public cells,
materials direction, provider contracts, and docs.
:::

:::{grid-item-card} Connect A Private Layout Repo
:link: home/ecosystem-workspace
:link-type: doc

Register a private provider in the same local environment without publishing
private layout/IP.
:::

:::{grid-item-card} Develop Ecosystem Features
:link: developing-features
:link-type: doc

Track reusable capability that may belong in `gsim`, `gplugins`, or this PDK.
:::

:::{grid-item-card} Prepare Upstream PRs
:link: home/ecosystem-workspace
:link-type: doc

Use personal prototype work as a source for focused `features/<topic>` and
`integration/<topic>` branches.
:::

:::{grid-item-card} Review Public/Private Boundaries
:link: home/ecosystem-workspace
:link-type: doc

Check which data may be documented publicly and which data must remain in the
private layout repository.
:::

::::

```{toctree}
:hidden:

home/ecosystem-workspace
home/pdk-responsibilities
```

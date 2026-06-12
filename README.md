# ili-scq-pdk

`ili-scq-pdk` is I-Li Chiu's public superconducting quantum/RF PDK for
GDSFactory. It is the public side of a split architecture for labs that need
private layout/IP but still want to contribute to the GDSFactory ecosystem.

The PDK owns public process semantics: layer maps, layer stacks, material
records, cross-sections, public demo cells, and the layout-provider extension
contract. Solver workflow capability is integrated through public ecosystem
repositories and editable local contribution branches rather than copied into
the PDK core.

Private chip layouts do not live in this repository. Put private components,
parameters, GDS inputs, and design factories in a separate layout pack that
depends on this PDK.

## Architecture Goal

The first public milestone for this repository is documentation, repo
architecture, and docs publishing. It is not a migration of private solver
features into the public PDK.

The intended split is:

- `ili-scq-pdk`: public PDK, materials DB direction, technology/layerstack,
  layer semantics, public examples, and the private layout provider contract.
- `NCUAS_SC_Qubit_Design`: private layout/IP repository and first real consumer
  of the provider model. It keeps its existing documents as the detailed record
  of current private capabilities.
- `Quantum-RF-PDK`: ecosystem reference and contribution target when a new
  public simulation method belongs there.
- `gsim`: primary target for solver workflow improvements, Palace analysis,
  reporting, benchmark support, and material-schema integration that should be
  reusable beyond one PDK.
- `gplugins`: target for GDSFactory plugin integration that belongs in the
  broader plugin ecosystem.

## Use the Open PDK

The package follows the GDSFactory+/Quantum-RF-PDK discovery shape:

```text
ili_scq_pdk/
  cells/
  samples/
  models/
  klayout/
```

`ili_scq_pdk.cells` is the public cell registry. `ili_scq_pdk.models` is a
reserved namespace and exposes no model APIs yet.

Install the package in editable mode while developing:

```bash
git clone <your-fork-url> ili-scq-pdk
cd ili-scq-pdk
uv sync -p 3.12 --extra dev
```

For GDSFactory+ preview in VSCode, install the extension runtime extra into
the same project environment:

```bash
uv sync -p 3.12 --extra dev --extra gdsfactoryplus
```

If you also want local docs in the same environment, include the docs group:

```bash
uv sync -p 3.12 --group docs --extra dev --extra gdsfactoryplus
```

Activate the PDK and build a public demo component:

```python
import ili_scq_pdk
from ili_scq_pdk.cells import cpw_straight

ili_scq_pdk.activate()

component = cpw_straight(length=500, signal_width=10, gap=6)
component.show()
```

The public layout provider API exposes demo designs without requiring any
private repository:

```python
from ili_scq_pdk.layouts import LayoutRequest, available_public_layout_providers
from ili_scq_pdk.layouts import load_layout_provider

print(available_public_layout_providers())

provider = load_layout_provider("public.ili_cpw_demo")
case = provider.build_layout(LayoutRequest(layout_id="cpw_straight"))
case.component.show()
```

## Create Your Own Private Layout Pack

Create a separate private repository for real designs:

```text
my-lab-layouts/
  pyproject.toml
  src/my_lab_layouts/
    __init__.py
    provider.py
    cells.py
```

Depend on the PDK:

```toml
[project]
name = "my-lab-layouts"
dependencies = ["ili-scq-pdk"]

[project.entry-points."ili_scq_pdk.layout_providers"]
"private.reference_design" = "my_lab_layouts.provider:get_provider"
```

Implement a provider:

```python
from ili_scq_pdk.layouts import LayoutCase, LayoutProviderMetadata, LayoutRequest


class MyLabProvider:
    provider_id = "private.reference_design"
    visibility = "private_layout"

    def describe(self):
        return LayoutProviderMetadata(
            provider_id=self.provider_id,
            visibility=self.visibility,
            summary="Private layout pack selected outside the public PDK.",
            package_name="my_lab_layouts",
        )

    def build_layout(self, request: LayoutRequest):
        component = build_private_component(request)
        return LayoutCase(
            provider=self.describe(),
            layout_id=request.layout_id,
            component=component,
            layer_stack=None,
        )


def get_provider(provider_id="private.reference_design"):
    if provider_id != "private.reference_design":
        raise KeyError(provider_id)
    return MyLabProvider()
```

After installing the private package, public workflow code can load the provider
by id. Without access to the private repository, the import and entry point are
not available, so the private layout remains invisible.

## Forking the PDK And Ecosystem Repos

Fork `ili-scq-pdk` when you need to change public process semantics: layers,
layer stack, material policies, port conventions, provider API, or public
component primitives.

Do not fork the PDK only to add private chip designs. Ordinary private designs
belong in a layout pack registered through `ili_scq_pdk.layout_providers`.

Use documented local path sources for ecosystem work instead of ad hoc editable
installs. For a local workspace with sibling public forks and an optional
private layout pack, add dependency groups and `uv` sources like:

```toml
[dependency-groups]
ecosystem = [
  "gsim",
  "gplugins",
  "qpdk",
]
private-layout = [
  "i-li-chiu-scq-layouts-private",
]

[tool.uv.sources]
gsim = { path = "../gsim", editable = true }
gplugins = { path = "../gplugins", editable = true }
qpdk = { path = "../quantum-rf-pdk", editable = true }
i-li-chiu-scq-layouts-private = { path = "../../NCUAS_SC_Qubit_Design/i-li-chiu-scq-layouts-private", editable = true }
```

The checkout folder is `quantum-rf-pdk`, but the Python distribution name is
`qpdk`.

Then sync the workspace environment from `ili-scq-pdk`:

```bash
uv sync -p 3.12 --group docs --extra dev --extra gdsfactoryplus --group ecosystem --group private-layout
```

The `private-layout` group is for local/private workspaces. Public CI and public
docs builds should not require it.

Prototype broad solver changes on personal branches in `gsim` and `gplugins`.
After the PDK-facing workflow is accepted, slice the work into focused upstream
integration branches that a human reviewer can inspect without private layout
context.

## Repository Boundaries

- `ili-scq-pdk`: public process, material records, technology/layerstack, and
  layout-provider API.
- private layout pack: private cells, design factories, layout parameters, GDS
  inputs from private designs, private run evidence, and lab-specific notebooks.
- `gsim` and `gplugins`: reusable simulation and plugin capability developed
  through fork/editable contribution workflows.

This split lets collaborators review the PDK and workflow without seeing
private layout IP.

## Formal Support Direction

The public PDK is responsible for making these workflows supportable, even when
the implementation belongs upstream:

- Palace electrostatic, EPR, and reporting support.
- Benchmark and performance analysis surfaces for solver cost control.
- Materials DB and material-schema integration, including preservation of
  `materials.json` style data sources when they are introduced.

The PDK should expose process/material/layer semantics and provider contracts.
It should not become a monolithic solver workflow repository.

## Documentation

The documentation scaffold follows the publication pattern used by
Quantum-RF-PDK without copying its branding:

- `notebooks/src/` stores Jupytext source notebooks.
- `docs/notebooks.rst` curates notebook entries.
- `docs/docs.just` provides notebook conversion, HTML docs, LaTeX docs, and PDF
  docs targets.
- `.github/workflows/pages.yml` builds docs on pull requests and deploys Pages
  from `main`.

Build the docs locally with:

```bash
uv sync -p 3.12 --group docs --extra dev
just docs
just docs-latex
just docs-pdf
```

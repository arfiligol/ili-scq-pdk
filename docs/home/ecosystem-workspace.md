# Ecosystem Workspace And Contribution Loop

`ili-scq-pdk` is designed for contributors who need private Primary Layout
repositories but still want to validate and upstream reusable public
infrastructure. The private repo proves that the workflow works on real layouts.
The public repos carry the reusable process, provider, simulation, and plugin
contracts that can be reviewed without private layout/IP.

## Workspace Shape

Use sibling checkouts so each repo keeps its own ownership boundary:

```text
SCQ_Design/
  GDSFactory_Community_Workbench/
    ili-scq-pdk/
    gsim/
    gplugins/
    quantum-rf-pdk/
  NCUAS_SC_Qubit_Design/
    i-li-chiu-scq-layouts-private/
```

| Repo or folder | Responsibility |
| --- | --- |
| `ili-scq-pdk` | Public SCQ PDK: layer/process/material semantics, `LAYER_STACK`, public cells, provider contract, public examples, docs. |
| private layout repo | Primary Layout, private cells, private parameters, GDS inputs from private designs, private notebooks, private run evidence. |
| `gsim` | Reusable solver workflow, Palace/EPR/reporting capability, benchmark surfaces, material workflow adapters. |
| `gplugins` | Generic GDSFactory plugin capability and helper surfaces that should not be PDK-specific. |
| `quantum-rf-pdk` | Public reference and possible contribution target; it is not the upstream of `ili-scq-pdk`. |

## Create The Workspace

Clone public forks under the public workbench:

```bash
mkdir -p SCQ_Design/GDSFactory_Community_Workbench
cd SCQ_Design/GDSFactory_Community_Workbench
git clone <your-ili-scq-pdk-fork-url> ili-scq-pdk
git clone <your-gsim-fork-url> gsim
git clone <your-gplugins-fork-url> gplugins
git clone <your-quantum-rf-pdk-fork-url> quantum-rf-pdk
```

Keep private layout packs in a sibling private workspace:

```bash
mkdir -p ../NCUAS_SC_Qubit_Design
cd ../NCUAS_SC_Qubit_Design
git clone <your-private-layout-repo-url> i-li-chiu-scq-layouts-private
```

The private checkout may also be a private submodule, a local symlink, or an
ignored local folder if a lab wants that source-location pattern. Those are
optional local workspace choices. The public PDK contract is still provider
discovery in the same Python environment, not ownership of private source code.

## Sync The Python Environment

For a reproducible local ecosystem environment, document path dependencies in a
local `pyproject.toml` edit instead of running ad hoc editable installs:

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
`qpdk`; `uv` requires the dependency name to match the package metadata.

Then sync one environment from `ili-scq-pdk`:

```bash
cd SCQ_Design/GDSFactory_Community_Workbench/ili-scq-pdk
uv sync -p 3.12 --group docs --extra dev --extra gdsfactoryplus --group ecosystem --group private-layout
```

The `private-layout` group is a local/private workspace setup. Public CI and
public docs builds must not require it.

For GDSFactory+ preview in VSCode, open `ili-scq-pdk` as the active folder and
select this interpreter:

```text
ili-scq-pdk/.venv/bin/python3
```

## Provider Abstraction Boundary

The provider contract lets public code load a private layout pack when that pack
is installed locally, while keeping process semantics in the public PDK.

Ownership is split deliberately:

- private provider owns the `Component`, `layout_id`, and public-safe metadata;
- `ili-scq-pdk` owns `LAYER`, `LAYER_VIEWS`, `LAYER_STACK`,
  material/process semantics, and provider discovery;
- `gsim` consumes the component, public PDK layer stack, and public-safe
  metadata at its solver workflow boundary.

Do not model the private provider as the owner of the process stack. The layer
stack is part of the public process contract unless a future public PDK
extension explicitly changes it. A private provider may pass through the public
PDK `LAYER_STACK`; it should not define a separate private process stack.

A private package registers itself through the existing entry point group:

```toml
[project.entry-points."ili_scq_pdk.layout_providers"]
"private.reference_design" = "my_lab_layouts.provider:get_provider"
```

The public PDK can then discover it by id:

```python
from ili_scq_pdk.layouts import load_layout_provider

provider = load_layout_provider("private.reference_design")
```

Without the private package installed in the active environment, the provider is
not importable and the private layout remains unavailable.

## Personal Branches And PR Branches

Use a long-lived personal branch as the prototype log:

```bash
git switch -c i-li-chiu upstream/main
```

Keep commits topical and cherry-pickable. A useful prototype commit should be
able to move into a public PR branch without private layout/IP, private
parameters, private notebooks, or private run evidence.

When a public slice is ready, create a clean PR branch from the target upstream
base:

```bash
git fetch upstream
git switch -c features/<topic> upstream/main
git cherry-pick -x <accepted-public-commit>
```

Use `features/<topic>` or `integration/<topic>` for PR branches. These branches
should contain only public implementation, tests, docs, and public-safe evidence
that reviewers can inspect without access to the private layout repo.

## Public/Private Checklist

Public docs, tests, and examples may include:

- public process and layer semantics;
- public material records and aliases;
- provider interfaces and public demo providers;
- public cells, public samples, and publication-safe notebooks;
- upstream contribution instructions and public benchmark methodology.

They must not include:

- private qubit or resonator geometry;
- private layout parameters;
- GDS inputs from private designs;
- private notebooks or private run evidence;
- benchmark values from private layouts unless explicitly cleared for
  publication;
- lab-specific implementation details that reveal private layout/IP.

## Where Changes Belong

| Change | Destination |
| --- | --- |
| Layer names, layer views, layer stack, process semantics | `ili-scq-pdk` |
| Public SCQ material records and provider contract | `ili-scq-pdk` |
| Private cells, Primary Layout factories, GDS inputs from private designs | private layout repo |
| Reusable Palace/EPR/reporting workflow | `gsim` |
| Reusable benchmark and solver cost workflow | `gsim` |
| Generic GDSFactory plugin integration | `gplugins` |
| Quantum/RF public reference method matching that project scope | `quantum-rf-pdk`, when appropriate |

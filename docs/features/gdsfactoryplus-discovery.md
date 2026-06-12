# GDSFactory+ PDK Discovery

**Target:** `ili-scq-pdk`

**Status:** prototype

The PDK should remain discoverable when opened as the active VSCode folder with
the GDSFactory+ extension.

Required shape:

- flat package layout;
- public `ili_scq_pdk.cells` registry;
- public `ili_scq_pdk.samples`;
- reserved `ili_scq_pdk.models`;
- `[tool.gdsfactoryplus]` metadata in `pyproject.toml`.

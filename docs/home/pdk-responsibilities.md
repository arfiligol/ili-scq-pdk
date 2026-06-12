# PDK Responsibilities

`ili-scq-pdk` owns the public SCQ process contract. Private layout repos may
use this contract, but they do not own or redefine it.

The PDK-owned surface includes:

- material records and aliases;
- layer maps and layer views;
- technology and `LAYER_STACK`;
- public cells and samples;
- provider contracts;
- docs and notebooks that expose workflow shape without private layout/IP.

Reusable solver workflow belongs upstream whenever possible:

- `gsim`: Palace electrostatic, EPR, reporting, benchmarks, material resolver
  adapters, and workflow orchestration reusable across PDKs.
- `gplugins`: generic GDSFactory plugin integration.
- `Quantum-RF-PDK`: reference and possible contribution target when a feature
  belongs to the public quantum/RF PDK scope.

Private layout/IP belongs in a separate private layout repo. A private provider
may return a `Component`, `layout_id`, and public-safe metadata, but the public
PDK remains the owner of layer and process semantics.

See {doc}`ecosystem-workspace` for the local workspace and contribution loop.

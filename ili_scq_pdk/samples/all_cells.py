"""Sample that places every public PDK cell."""

from __future__ import annotations

import gdsfactory as gf

from ili_scq_pdk import PDK, activate


@gf.cell
def all_public_cells(spacing: float = 80.0) -> gf.Component:
    """Return a component containing one instance of each public PDK cell."""

    activate()
    component = gf.Component()
    x = 0.0
    for name in sorted(PDK.cells):
        reference = component << PDK.cells[name]()
        reference.movex(x - reference.xmin)
        x = reference.xmax + spacing
    return component

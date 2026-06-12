"""Public CPW primitives."""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import LayerSpec

from ili_scq_pdk.tech import LAYER


@gf.cell
def cpw_straight(
    length: float = 500.0,
    signal_width: float = 10.0,
    gap: float = 6.0,
    ground_width: float = 50.0,
    layer: LayerSpec = LAYER.D0_TOP_M1_DRAW,
) -> gf.Component:
    """Return a public CPW straight section with two simulation ports."""

    component = gf.Component()
    component << gf.components.rectangle(
        size=(length, signal_width),
        centered=True,
        layer=layer,
    )
    top_ground = component << gf.components.rectangle(
        size=(length, ground_width),
        centered=True,
        layer=layer,
    )
    top_ground.movey((signal_width + ground_width) / 2 + gap)
    bottom_ground = component << gf.components.rectangle(
        size=(length, ground_width),
        centered=True,
        layer=layer,
    )
    bottom_ground.movey(-((signal_width + ground_width) / 2 + gap))
    component.add_port(
        name="o1",
        center=(-length / 2, 0),
        width=signal_width,
        orientation=180,
        layer=layer,
        port_type="sim_cpw",
    )
    component.add_port(
        name="o2",
        center=(length / 2, 0),
        width=signal_width,
        orientation=0,
        layer=layer,
        port_type="sim_cpw",
    )
    return component

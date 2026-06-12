"""Public capacitor primitives."""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import LayerSpec

from ili_scq_pdk.tech import LAYER


@gf.cell
def interdigital_capacitor(
    fingers: int = 6,
    finger_length: float = 120.0,
    finger_width: float = 6.0,
    finger_gap: float = 4.0,
    bus_width: float = 12.0,
    layer: LayerSpec = LAYER.D0_TOP_M1_DRAW,
) -> gf.Component:
    """Return a generic public interdigital capacitor primitive."""

    if fingers < 2:
        raise ValueError("fingers must be at least 2.")
    pitch = finger_width + finger_gap
    height = (fingers - 1) * pitch + finger_width
    component = gf.Component()
    left_bus = component << gf.components.rectangle(
        size=(bus_width, height),
        centered=True,
        layer=layer,
    )
    left_bus.movex(-finger_length / 2)
    right_bus = component << gf.components.rectangle(
        size=(bus_width, height),
        centered=True,
        layer=layer,
    )
    right_bus.movex(finger_length / 2)

    y0 = -height / 2 + finger_width / 2
    for index in range(fingers):
        finger = component << gf.components.rectangle(
            size=(finger_length, finger_width),
            centered=True,
            layer=layer,
        )
        finger.movey(y0 + index * pitch)
        finger.movex(0 if index % 2 == 0 else bus_width / 2)

    component.add_port(
        name="left",
        center=(-finger_length / 2 - bus_width / 2, 0),
        width=bus_width,
        orientation=180,
        layer=layer,
        port_type="sim_lumped",
    )
    component.add_port(
        name="right",
        center=(finger_length / 2 + bus_width / 2, 0),
        width=bus_width,
        orientation=0,
        layer=layer,
        port_type="sim_lumped",
    )
    return component

"""Simulation port type registration for the open PDK."""

from __future__ import annotations

import gdsfactory as gf

SIM_PORT_TYPES = (
    "sim_cpw",
    "sim_lumped",
    "sim_wave",
    "sim_mesh",
    "sim_junction_lumped",
)


def register_sim_port_types() -> None:
    """Register public simulation port types with GDSFactory."""

    for port_type in SIM_PORT_TYPES:
        if port_type not in gf.CONF.port_types:
            gf.CONF.port_types += (port_type,)

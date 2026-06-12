"""PDK construction and activation."""

from functools import lru_cache
from typing import cast

from gdsfactory.cross_section import get_cross_sections
from gdsfactory.get_factories import get_cells
from gdsfactory.pdk import Pdk
from gdsfactory.typings import ComponentFactory

from ili_scq_pdk import cells, tech
from ili_scq_pdk.ports import register_sim_port_types

_cells = cast(dict[str, ComponentFactory], get_cells(cells))
_cross_sections = get_cross_sections(tech)


@lru_cache
def get_pdk() -> Pdk:
    """Return the open superconducting quantum/RF PDK."""

    register_sim_port_types()
    return Pdk(
        name="ili_scq_pdk",
        cells=_cells,
        cross_sections=_cross_sections,
        layers=tech.LAYER,
        layer_stack=tech.LAYER_STACK,
        layer_views=tech.LAYER_VIEWS,
        connectivity=tech.LAYER_CONNECTIVITY,
        routing_strategies=tech.routing_strategies,
    )


PDK = get_pdk()


def activate() -> Pdk:
    """Activate the open PDK and return it."""

    PDK.activate()
    return PDK

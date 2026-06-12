"""Provider-safe public PDK usage sample."""

from __future__ import annotations

import gdsfactory as gf

from ili_scq_pdk.layouts import LayoutRequest, load_layout_provider


@gf.cell
def public_provider_demo(layout_id: str = "cpw_straight") -> gf.Component:
    """Build a public layout through the same provider contract private repos use."""

    provider = load_layout_provider("public.ili_cpw_demo")
    case = provider.build_layout(LayoutRequest(layout_id=layout_id))
    return case.component

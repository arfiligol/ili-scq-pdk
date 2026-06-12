# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
# ---

# %% [markdown]
# # Public PDK quickstart
#
# This notebook demonstrates the open PDK surface that is safe to publish:
# process semantics, public demo components, and the layout-provider extension
# point. Private chip layouts and private GDS inputs are intentionally outside
# this repository.

# %%
from IPython.display import display

import ili_scq_pdk
from ili_scq_pdk.cells import cpw_straight, interdigital_capacitor
from ili_scq_pdk.layouts import (
    LayoutRequest,
    available_public_layout_providers,
    load_layout_provider,
)

ili_scq_pdk.activate()


def port_names(component):
    return sorted(port.name for port in component.ports)


# %% [markdown]
# ## Public demo cells
#
# The PDK can create small public superconducting RF primitives without loading
# any private layout package.

# %%
cpw = cpw_straight(length=500, signal_width=10, gap=6)
capacitor = interdigital_capacitor(fingers=6)

display(
    {
        "cpw": {"name": cpw.name, "ports": port_names(cpw)},
        "capacitor": {"name": capacitor.name, "ports": port_names(capacitor)},
    }
)

# %% [markdown]
# ## Public layout provider
#
# Workflows consume layouts through provider IDs. The built-in public provider
# exposes demo layouts for documentation and smoke tests.

# %%
public_providers = available_public_layout_providers()
display(public_providers)

# %%
provider = load_layout_provider("public.ili_cpw_demo")
case = provider.build_layout(LayoutRequest(layout_id="quarter_wave_resonator"))

display(
    {
        "provider": case.provider.provider_id,
        "visibility": case.provider.visibility,
        "layout_id": case.layout_id,
        "component": case.component.name,
        "ports": sorted(case.ports),
    }
)

# %% [markdown]
# ## Private layout boundary
#
# Private designs should be packaged separately and registered through the same
# provider entry-point group. This notebook does not import or name any private
# layout package.

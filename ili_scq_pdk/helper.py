"""Small helper functions for PDK tests and docs examples."""

from __future__ import annotations

from gdsfactory.technology import LayerViews
from gdsfactory.typings import Layer


def layer_views_to_tuples(layer_views: LayerViews) -> dict[str, Layer]:
    """Return layer-view names mapped to concrete ``(layer, datatype)`` tuples."""

    return {
        name: layer_view.layer
        for name, layer_view in layer_views.layer_views.items()
        if layer_view.layer is not None
    }

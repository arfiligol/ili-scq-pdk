"""Provider contracts for public and private layout packs."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import gdsfactory as gf
from gdsfactory.technology import LayerStack


@dataclass(frozen=True, slots=True)
class LayoutProviderMetadata:
    """Metadata describing the owner and visibility of a layout provider."""

    provider_id: str
    visibility: str
    summary: str
    package_name: str
    source: str = "python-package"


@dataclass(frozen=True, slots=True)
class LayoutRequest:
    """Request for a layout from a provider."""

    layout_id: str = "cpw_straight"
    settings: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class LayoutCase:
    """Provider-produced layout data without solver-specific dependencies."""

    provider: LayoutProviderMetadata
    layout_id: str
    component: gf.Component
    layer_stack: LayerStack | None
    ports: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class LayoutProvider(Protocol):
    """Protocol implemented by public demos and private layout packs."""

    provider_id: str
    visibility: str

    def describe(self) -> LayoutProviderMetadata:
        """Return provider metadata."""

    def build_layout(self, request: LayoutRequest) -> LayoutCase:
        """Build a layout case for a public workflow."""

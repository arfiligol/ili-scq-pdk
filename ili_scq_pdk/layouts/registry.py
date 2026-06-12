"""Layout provider discovery."""

from __future__ import annotations

import importlib.metadata as metadata
from typing import Any

from .provider import LayoutProvider

LAYOUT_PROVIDER_ENTRY_POINT_GROUP = "ili_scq_pdk.layout_providers"

_PUBLIC_PROVIDER_IDS = ("public.ili_cpw_demo",)


class LayoutProviderError(LookupError):
    """Raised when a layout provider cannot be loaded."""


def available_public_layout_providers() -> tuple[str, ...]:
    """Return public provider ids bundled with this PDK."""

    return _PUBLIC_PROVIDER_IDS


def load_layout_provider(provider_id: str = "public.ili_cpw_demo") -> LayoutProvider:
    """Load a bundled public provider or an installed layout-pack provider."""

    if provider_id in _PUBLIC_PROVIDER_IDS:
        from ili_scq_pdk.demo.provider import get_provider

        return get_provider(provider_id)

    entry_point = _find_entry_point(provider_id)
    if entry_point is None:
        known = ", ".join(available_public_layout_providers())
        raise LayoutProviderError(
            f"Unknown layout provider {provider_id!r}. Known public providers: {known}."
        )
    provider = _provider_from_entry_point(entry_point, provider_id)
    _validate_provider(provider, provider_id)
    return provider


def _find_entry_point(provider_id: str) -> metadata.EntryPoint | None:
    entry_points = metadata.entry_points()
    if hasattr(entry_points, "select"):
        candidates = entry_points.select(group=LAYOUT_PROVIDER_ENTRY_POINT_GROUP)
    else:
        candidates = entry_points.get(LAYOUT_PROVIDER_ENTRY_POINT_GROUP, ())
    for entry_point in candidates:
        if entry_point.name == provider_id:
            return entry_point
    return None


def _provider_from_entry_point(
    entry_point: metadata.EntryPoint,
    provider_id: str,
) -> LayoutProvider:
    loaded = entry_point.load()
    if not callable(loaded):
        raise LayoutProviderError(
            f"Layout provider entry point {entry_point.name!r} must load a callable."
        )
    factory = loaded
    try:
        provider = factory(provider_id)
    except TypeError:
        provider = factory()
    return provider


def _validate_provider(provider: Any, provider_id: str) -> None:
    required_methods = ("describe", "build_layout")
    missing = [name for name in required_methods if not callable(getattr(provider, name, None))]
    if missing:
        joined = ", ".join(missing)
        raise LayoutProviderError(f"Layout provider {provider_id!r} is missing: {joined}.")
    if getattr(provider, "provider_id", provider_id) != provider_id:
        raise LayoutProviderError(
            f"Layout provider entry point {provider_id!r} returned provider_id "
            f"{getattr(provider, 'provider_id', None)!r}."
        )
    visibility = getattr(provider, "visibility", None)
    if provider_id.startswith("private.") and visibility != "private_layout":
        raise LayoutProviderError(
            f"Private provider {provider_id!r} must declare visibility='private_layout'."
        )

"""Public layout provider bundled with the open PDK."""

from __future__ import annotations

from dataclasses import dataclass

from ili_scq_pdk.cells import cpw_straight, interdigital_capacitor, quarter_wave_resonator
from ili_scq_pdk.layouts.provider import LayoutCase, LayoutProviderMetadata, LayoutRequest
from ili_scq_pdk.tech import LAYER_STACK


@dataclass(frozen=True, slots=True)
class IliPublicDemoProvider:
    """Public demo provider for workflow smoke tests and examples."""

    provider_id: str = "public.ili_cpw_demo"
    visibility: str = "public"

    def describe(self) -> LayoutProviderMetadata:
        return LayoutProviderMetadata(
            provider_id=self.provider_id,
            visibility=self.visibility,
            summary="Public CPW and capacitor demos from ili-scq-pdk.",
            package_name="ili_scq_pdk",
        )

    def build_layout(self, request: LayoutRequest) -> LayoutCase:
        from ili_scq_pdk import activate

        activate()
        layout_id = request.layout_id or "cpw_straight"
        settings = dict(request.settings)
        if layout_id == "cpw_straight":
            component = cpw_straight(**settings)
        elif layout_id == "interdigital_capacitor":
            component = interdigital_capacitor(**settings)
        elif layout_id == "quarter_wave_resonator":
            component = quarter_wave_resonator(**settings)
        else:
            raise KeyError(f"Unknown public demo layout_id {layout_id!r}.")
        return LayoutCase(
            provider=self.describe(),
            layout_id=layout_id,
            component=component,
            layer_stack=LAYER_STACK,
            ports=tuple(port.name for port in component.ports),
            metadata={"visibility": self.visibility},
        )


def get_provider(provider_id: str = "public.ili_cpw_demo") -> IliPublicDemoProvider:
    """Return the built-in public demo provider."""

    if provider_id != "public.ili_cpw_demo":
        raise KeyError(provider_id)
    return IliPublicDemoProvider(provider_id=provider_id)

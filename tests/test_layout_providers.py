from __future__ import annotations

import importlib.metadata as metadata

from ili_scq_pdk.cells import cpw_straight
from ili_scq_pdk.layouts import (
    LayoutCase,
    LayoutProviderMetadata,
    LayoutRequest,
    available_public_layout_providers,
    load_layout_provider,
)
from ili_scq_pdk.layouts.registry import LAYOUT_PROVIDER_ENTRY_POINT_GROUP


def test_public_provider_loads_public_demo_case() -> None:
    assert available_public_layout_providers() == ("public.ili_cpw_demo",)

    provider = load_layout_provider("public.ili_cpw_demo")
    case = provider.build_layout(LayoutRequest(layout_id="cpw_straight"))

    assert case.provider.provider_id == "public.ili_cpw_demo"
    assert case.provider.visibility == "public"
    assert case.component.ports
    assert case.layer_stack is not None


def test_entry_point_private_provider_is_first_class(monkeypatch) -> None:
    class FakePrivateProvider:
        provider_id = "private.fake_lab"
        visibility = "private_layout"

        def describe(self) -> LayoutProviderMetadata:
            return LayoutProviderMetadata(
                provider_id=self.provider_id,
                visibility=self.visibility,
                summary="Fake private layout provider for tests.",
                package_name="fake_lab_layouts",
            )

        def build_layout(self, request: LayoutRequest) -> LayoutCase:
            return LayoutCase(
                provider=self.describe(),
                layout_id=request.layout_id,
                component=cpw_straight(),
                layer_stack=None,
            )

    class FakeEntryPoint:
        name = "private.fake_lab"
        group = LAYOUT_PROVIDER_ENTRY_POINT_GROUP

        def load(self):
            return lambda provider_id: FakePrivateProvider()

    monkeypatch.setattr(
        metadata,
        "entry_points",
        lambda: {LAYOUT_PROVIDER_ENTRY_POINT_GROUP: [FakeEntryPoint()]},
    )

    provider = load_layout_provider("private.fake_lab")
    case = provider.build_layout(LayoutRequest(layout_id="reference"))

    assert provider.visibility == "private_layout"
    assert case.provider.package_name == "fake_lab_layouts"

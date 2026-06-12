from __future__ import annotations

import gdsfactory as gf

import ili_scq_pdk
from ili_scq_pdk import PDK, cells, config, models, samples, tech


def test_qpdk_style_public_import_surface() -> None:
    assert ili_scq_pdk.PATH == config.PATH
    assert cells.cpw_straight
    assert cells.interdigital_capacitor
    assert cells.quarter_wave_resonator
    assert (tech.LAYER.D0_TOP_M1_DRAW.layer, tech.LAYER.D0_TOP_M1_DRAW.datatype) == (1, 0)
    assert models.__all__ == []
    assert samples.all_public_cells


def test_pdk_registry_contains_public_cells() -> None:
    expected = {"cpw_straight", "interdigital_capacitor", "quarter_wave_resonator"}

    assert expected <= set(PDK.cells)


def test_gdsfactory_get_component_works_after_activation() -> None:
    ili_scq_pdk.activate()

    assert gf.get_component("cpw_straight").name.startswith("cpw_straight")
    assert gf.get_component("interdigital_capacitor").ports
    assert gf.get_component("quarter_wave_resonator").ports


def test_public_samples_generate_components() -> None:
    functions = ili_scq_pdk.get_sample_functions()

    assert "ili_scq_pdk.samples.all_cells.all_public_cells" in functions
    assert "ili_scq_pdk.samples.provider_safe_usage.public_provider_demo" in functions
    for function in functions.values():
        component = function()
        assert component.name
        assert component.ports or len(component.insts) > 0

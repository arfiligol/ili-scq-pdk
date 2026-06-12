from pathlib import Path

import ili_scq_pdk
from ili_scq_pdk.cells import cpw_straight, interdigital_capacitor
from ili_scq_pdk.tech import LAYER_STACK


def test_pdk_activates_and_builds_public_cells() -> None:
    pdk = ili_scq_pdk.activate()

    assert pdk.name == "ili_scq_pdk"
    assert "D0_TOP_M1" in LAYER_STACK.layers
    assert cpw_straight().ports
    assert interdigital_capacitor().ports


def test_public_pdk_has_no_private_imports_or_gds() -> None:
    package_root = Path(__file__).resolve().parents[1] / "ili_scq_pdk"
    source_text = "\n".join(path.read_text() for path in package_root.rglob("*.py"))

    assert "ncuas_designs" not in source_text
    assert "AS Reference" not in source_text
    assert "AS Circular" not in source_text
    assert not list(package_root.rglob("*.gds"))

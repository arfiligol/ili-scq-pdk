"""Public technology definitions for the open superconducting PDK."""

from collections.abc import Callable

import gdsfactory as gf
from gdsfactory.cross_section import CrossSection, cross_section
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack, LayerView, LayerViews
from gdsfactory.typings import ConnectivitySpec, Layer

nm = 1e-3


class LayerMapILISCQPDK(LayerMap):
    """Die and face aware public layer map.

    Layer names intentionally describe process semantics only. Real private
    qubit, resonator, and chip assemblies should live in layout packs.
    """

    D0_BOTTOM_M1_DRAW: Layer = (3, 0)
    D0_BOTTOM_M1_ETCH: Layer = (3, 1)
    D0_TOP_M1_DRAW: Layer = (1, 0)
    D0_TOP_M1_ETCH: Layer = (1, 1)
    D1_BOTTOM_M1_DRAW: Layer = (2, 0)
    D1_BOTTOM_M1_ETCH: Layer = (2, 1)
    D1_TOP_M1_DRAW: Layer = (4, 0)
    D1_TOP_M1_ETCH: Layer = (4, 1)

    D0_D1_INDIUM_BUMP: Layer = (40, 0)
    D0_D1_UNDER_BUMP: Layer = (40, 1)

    D0_BOTTOM_AB_DRAW: Layer = (12, 0)
    D0_BOTTOM_AB_VIA: Layer = (12, 1)
    D0_TOP_AB_DRAW: Layer = (10, 0)
    D0_TOP_AB_VIA: Layer = (10, 1)
    D1_BOTTOM_AB_DRAW: Layer = (11, 0)
    D1_BOTTOM_AB_VIA: Layer = (11, 1)
    D1_TOP_AB_DRAW: Layer = (13, 0)
    D1_TOP_AB_VIA: Layer = (13, 1)

    D0_BOTTOM_JJ_DRAW: Layer = (20, 0)
    D0_TOP_JJ_DRAW: Layer = (21, 0)
    D1_BOTTOM_JJ_DRAW: Layer = (22, 0)
    D1_TOP_JJ_DRAW: Layer = (23, 0)

    D0_TOP_IND: Layer = (30, 0)
    D1_BOTTOM_IND: Layer = (30, 1)
    D0_TOP_TSV: Layer = (31, 0)
    D1_BOTTOM_TSV: Layer = (31, 1)
    DICE: Layer = (70, 0)

    D0_BOTTOM_ALN: Layer = (81, 0)
    D0_TOP_ALN: Layer = (80, 0)
    D1_BOTTOM_ALN: Layer = (83, 0)
    D1_TOP_ALN: Layer = (82, 0)

    D0_BOTTOM_GROUND_MASK: Layer = (111, 0)
    D0_TOP_GROUND_MASK: Layer = (110, 0)
    D1_BOTTOM_GROUND_MASK: Layer = (110, 1)
    D1_TOP_GROUND_MASK: Layer = (111, 1)

    TEXT: Layer = (90, 0)
    LABEL_SETTINGS: Layer = (100, 0)
    LABEL_INSTANCE: Layer = (101, 0)
    WG: Layer = (102, 0)
    ERROR_PATH: Layer = (1000, 0)

    D0_BOTTOM_M1_DOMAIN: Layer = (200, 0)
    D0_TOP_M1_DOMAIN: Layer = (200, 1)
    D1_BOTTOM_M1_DOMAIN: Layer = (200, 2)
    D1_TOP_M1_DOMAIN: Layer = (200, 3)
    D0_SUBSTRATE_AREA: Layer = (201, 0)
    D0_TO_D1_GAP_AREA: Layer = (201, 1)
    D1_SUBSTRATE_AREA: Layer = (201, 2)
    OUTER_VACUUM_AREA: Layer = (201, 3)
    D0_BOTTOM_SIM_BOUNDARY: Layer = (202, 0)
    D0_TOP_SIM_BOUNDARY: Layer = (202, 1)
    D1_BOTTOM_SIM_BOUNDARY: Layer = (202, 2)
    D1_TOP_SIM_BOUNDARY: Layer = (202, 3)


L = LAYER = LayerMapILISCQPDK

material_properties = {
    "vacuum": {"relative_permittivity": 1.0},
    "Si": {"relative_permittivity": 11.45},
    "Al": {"relative_permittivity": float("inf")},
    "Nb": {"relative_permittivity": float("inf")},
    "TiN": {"relative_permittivity": float("inf")},
    "In": {"relative_permittivity": float("inf")},
    "AlOx_native_generic": {"relative_permittivity": 10.0},
}

SUBSTRATE_THICKNESS_UM = 500.0
METAL_THICKNESS_UM = 200 * nm
AIRBRIDGE_VIA_THICKNESS_UM = 100 * nm
AIRBRIDGE_THICKNESS_UM = 200 * nm
D0_D1_METAL_FACE_GAP_UM = 9.8
D0_D1_SUBSTRATE_FACE_GAP_UM = D0_D1_METAL_FACE_GAP_UM + 2 * METAL_THICKNESS_UM
OUTER_VACUUM_THICKNESS_UM = 1000.0


def _zmin_from_face(*, face_z: float, outward: int, offset: float, thickness: float) -> float:
    if outward not in {-1, 1}:
        raise ValueError(f"outward must be -1 or +1, got {outward!r}.")
    if outward > 0:
        return face_z + offset
    return face_z - offset - thickness


def _face_layer_level(
    *,
    name: str,
    layer: Layer,
    face_z: float,
    outward: int,
    offset: float,
    thickness: float,
    material: str,
    mesh_order: int,
) -> LayerLevel:
    return LayerLevel(
        name=name,
        layer=layer,
        thickness=thickness,
        zmin=_zmin_from_face(
            face_z=face_z,
            outward=outward,
            offset=offset,
            thickness=thickness,
        ),
        material=material,
        mesh_order=mesh_order,
    )


def _face_layer_levels(
    *,
    die: str,
    face: str,
    face_z: float,
    outward: int,
    m1_domain_layer: Layer,
    m1_draw_layer: Layer,
    airbridge_draw_layer: Layer,
    airbridge_via_layer: Layer,
    sim_boundary_layer: Layer,
    mesh_order: int,
) -> dict[str, LayerLevel]:
    prefix = f"{die}_{face}"
    return {
        f"{prefix}_M1": _face_layer_level(
            name=f"{prefix}_M1",
            layer=m1_domain_layer,
            face_z=face_z,
            outward=outward,
            offset=0.0,
            thickness=METAL_THICKNESS_UM,
            material="Al",
            mesh_order=mesh_order,
        ),
        f"{prefix}_M1_DRAW": LayerLevel(
            name=f"{prefix}_M1_DRAW",
            layer=m1_draw_layer,
            thickness=0.0,
            zmin=face_z,
            material="Al",
            mesh_order=mesh_order,
        ),
        f"{prefix}_AB": _face_layer_level(
            name=f"{prefix}_AB",
            layer=airbridge_draw_layer,
            face_z=face_z,
            outward=outward,
            offset=2.0,
            thickness=AIRBRIDGE_THICKNESS_UM,
            material="Al",
            mesh_order=mesh_order - 1,
        ),
        f"{prefix}_AB_VIA": _face_layer_level(
            name=f"{prefix}_AB_VIA",
            layer=airbridge_via_layer,
            face_z=face_z,
            outward=outward,
            offset=0.0,
            thickness=AIRBRIDGE_VIA_THICKNESS_UM,
            material="Al",
            mesh_order=mesh_order - 1,
        ),
        f"{prefix}_SIM_BOUNDARY": LayerLevel(
            name=f"{prefix}_SIM_BOUNDARY",
            layer=sim_boundary_layer,
            thickness=0.0,
            zmin=face_z,
            material="Al",
            mesh_order=mesh_order,
        ),
    }


def get_layer_stack() -> LayerStack:
    """Return the public die and face aware layer stack."""

    d0_top_face_z = 0.0
    d0_bottom_face_z = -SUBSTRATE_THICKNESS_UM
    d1_bottom_face_z = D0_D1_SUBSTRATE_FACE_GAP_UM
    d1_substrate_zmin = d1_bottom_face_z
    d1_top_face_z = d1_substrate_zmin + SUBSTRATE_THICKNESS_UM

    return LayerStack(
        layers={
            "D0_SUBSTRATE": LayerLevel(
                name="D0_SUBSTRATE",
                layer=L.D0_SUBSTRATE_AREA,
                thickness=SUBSTRATE_THICKNESS_UM,
                zmin=-SUBSTRATE_THICKNESS_UM,
                material="Si",
                mesh_order=20,
            ),
            "D1_SUBSTRATE": LayerLevel(
                name="D1_SUBSTRATE",
                layer=L.D1_SUBSTRATE_AREA,
                thickness=SUBSTRATE_THICKNESS_UM,
                zmin=d1_substrate_zmin,
                material="Si",
                mesh_order=21,
            ),
            "D0_TO_D1_GAP": LayerLevel(
                name="D0_TO_D1_GAP",
                layer=L.D0_TO_D1_GAP_AREA,
                thickness=D0_D1_SUBSTRATE_FACE_GAP_UM,
                zmin=0.0,
                material="vacuum",
                mesh_order=98,
            ),
            "OUTER_VACUUM": LayerLevel(
                name="OUTER_VACUUM",
                layer=L.OUTER_VACUUM_AREA,
                thickness=OUTER_VACUUM_THICKNESS_UM,
                zmin=d1_top_face_z,
                material="vacuum",
                mesh_order=99,
            ),
            **_face_layer_levels(
                die="D0",
                face="BOTTOM",
                face_z=d0_bottom_face_z,
                outward=-1,
                m1_domain_layer=L.D0_BOTTOM_M1_DOMAIN,
                m1_draw_layer=L.D0_BOTTOM_M1_DRAW,
                airbridge_draw_layer=L.D0_BOTTOM_AB_DRAW,
                airbridge_via_layer=L.D0_BOTTOM_AB_VIA,
                sim_boundary_layer=L.D0_BOTTOM_SIM_BOUNDARY,
                mesh_order=11,
            ),
            **_face_layer_levels(
                die="D0",
                face="TOP",
                face_z=d0_top_face_z,
                outward=1,
                m1_domain_layer=L.D0_TOP_M1_DOMAIN,
                m1_draw_layer=L.D0_TOP_M1_DRAW,
                airbridge_draw_layer=L.D0_TOP_AB_DRAW,
                airbridge_via_layer=L.D0_TOP_AB_VIA,
                sim_boundary_layer=L.D0_TOP_SIM_BOUNDARY,
                mesh_order=10,
            ),
            **_face_layer_levels(
                die="D1",
                face="BOTTOM",
                face_z=d1_bottom_face_z,
                outward=-1,
                m1_domain_layer=L.D1_BOTTOM_M1_DOMAIN,
                m1_draw_layer=L.D1_BOTTOM_M1_DRAW,
                airbridge_draw_layer=L.D1_BOTTOM_AB_DRAW,
                airbridge_via_layer=L.D1_BOTTOM_AB_VIA,
                sim_boundary_layer=L.D1_BOTTOM_SIM_BOUNDARY,
                mesh_order=12,
            ),
            **_face_layer_levels(
                die="D1",
                face="TOP",
                face_z=d1_top_face_z,
                outward=1,
                m1_domain_layer=L.D1_TOP_M1_DOMAIN,
                m1_draw_layer=L.D1_TOP_M1_DRAW,
                airbridge_draw_layer=L.D1_TOP_AB_DRAW,
                airbridge_via_layer=L.D1_TOP_AB_VIA,
                sim_boundary_layer=L.D1_TOP_SIM_BOUNDARY,
                mesh_order=13,
            ),
            "D0_TOP_TSV": LayerLevel(
                name="D0_TOP_TSV",
                layer=L.D0_TOP_TSV,
                thickness=SUBSTRATE_THICKNESS_UM,
                zmin=-SUBSTRATE_THICKNESS_UM,
                material="TiN",
                mesh_order=3,
            ),
            "D1_BOTTOM_TSV": LayerLevel(
                name="D1_BOTTOM_TSV",
                layer=L.D1_BOTTOM_TSV,
                thickness=SUBSTRATE_THICKNESS_UM,
                zmin=d1_substrate_zmin,
                material="TiN",
                mesh_order=3,
            ),
            "D0_D1_INDIUM_BUMP": LayerLevel(
                name="D0_D1_INDIUM_BUMP",
                layer=L.D0_D1_INDIUM_BUMP,
                thickness=D0_D1_METAL_FACE_GAP_UM,
                zmin=METAL_THICKNESS_UM,
                material="In",
                mesh_order=3,
            ),
            "D0_D1_UNDER_BUMP": LayerLevel(
                name="D0_D1_UNDER_BUMP",
                layer=L.D0_D1_UNDER_BUMP,
                thickness=METAL_THICKNESS_UM,
                zmin=0.0,
                material="In",
                mesh_order=3,
            ),
        }
    )


def get_layer_views() -> LayerViews:
    """Return compact layer views for public demos."""

    layer_views = {
        "D0_TOP_M1_DRAW": LayerView(name="D0_TOP_M1_DRAW", layer=L.D0_TOP_M1_DRAW, color="gold"),
        "D1_BOTTOM_M1_DRAW": LayerView(
            name="D1_BOTTOM_M1_DRAW",
            layer=L.D1_BOTTOM_M1_DRAW,
            color="deepskyblue",
        ),
        "AIRBRIDGE": LayerView(name="AIRBRIDGE", layer=L.D0_TOP_AB_DRAW, color="violet"),
        "JUNCTION": LayerView(name="JUNCTION", layer=L.D0_TOP_JJ_DRAW, color="red"),
        "GROUND_MASK": LayerView(name="GROUND_MASK", layer=L.D0_TOP_GROUND_MASK, color="gray"),
        "TEXT": LayerView(name="TEXT", layer=L.TEXT, color="white"),
        "SIM_DOMAIN": LayerView(name="SIM_DOMAIN", layer=L.D0_TOP_M1_DOMAIN, color="green"),
    }
    return LayerViews(layer_views=layer_views)


def cpw(
    width: float = 10.0,
    gap: float = 6.0,
    layer: Layer = L.D0_TOP_M1_DRAW,
) -> CrossSection:
    """Return a signal-line cross-section for CPW-style public examples."""

    return cross_section(
        width=width,
        layer=layer,
        bbox_layers=(layer,),
        bbox_offsets=(gap,),
        port_names=("o1", "o2"),
        port_types=("electrical", "electrical"),
    )


LAYER_STACK = get_layer_stack()
LAYER_VIEWS = get_layer_views()
LAYER_CONNECTIVITY: list[ConnectivitySpec] = [
    ("D0_TOP_M1_DRAW", "D0_TOP_TSV", "D1_BOTTOM_M1_DRAW"),
    ("D0_TOP_M1_DRAW", "D0_D1_INDIUM_BUMP", "D1_BOTTOM_M1_DRAW"),
    ("D0_TOP_M1_DRAW", "D0_TOP_AB_DRAW", "D0_TOP_M1_DRAW"),
    ("D1_BOTTOM_M1_DRAW", "D1_BOTTOM_AB_DRAW", "D1_BOTTOM_M1_DRAW"),
]

routing_strategies: dict[str, Callable[..., object]] = {}

gf.CONF.layer_error_path = L.ERROR_PATH

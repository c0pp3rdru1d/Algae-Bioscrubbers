from __future__ import annotations

from .params import ReactorParams


def conservative_small() -> ReactorParams:
    # 2 m², 10 g/m²/day, 70% uptime
    return ReactorParams(
        area_m2=2.0,
        productivity_g_m2_day=10.0,
        c02_per_biomass=1.8,
        uptime_fraction=0.7,
    )


def realistic_medium() -> ReactorParams:
    # 4 m², 20 g/m²/day, 80% uptime
    return ReactorParams(
        area_m2=4.0,
        productivity_g_m2_day=20.0,
        c02_per_biomass=1.8,
        uptime_fraction=0.8,
    )


def optimized_large() -> ReactorParams:
    # 8 m², 27 g/m²/day, 85% uptime
    return ReactorParams(
        area_m2=8.0,
        productivity_g_m2_day=27.0,
        c02_per_biomass=1.8,
        uptime_fraction=0.85,
    )


SCENARIO_MAP = {
    "conservative_small": conservative_small,
    "realistic_medium": realistic_medium,
    "optimized_large": optimized_large,
}


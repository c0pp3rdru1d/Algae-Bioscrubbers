from dataclasses import dataclass


@dataclass
class EnergyParams:
    """
    Parameters describing clean energy available to each reactor.

    All units:
      - clean_kwh_per_year: total clean energy available per reactor per year
                            (from wave, solar, etc.)
      - lighting_fraction:  fraction (0–1) of that energy spent on LEDs.
                            The rest is assumed to go to pumps/mixing/etc.
    """
    clean_kwh_per_year: float
    lighting_fraction: float = 0.0  # default: no lighting


from dataclasses import dataclass

@dataclass
class ReactorParams:
    """

    Parameters describing a single household algae bio-reactor.

    All units:
        - area_m2: square meters (m**2) 
        - productivity_g_m2_day: grams of dry biomass per M**2 per day 
        - c02_per_biomass: grams C02 fixed per gram dry c02_per_biomass
        - uptime_fraction: fraction of time the system is actually running
                                        (0.7 = 70% of the year)
    """

    area_m2: float
    productivity_g_m2_day: float
    c02_per_biomass: float = 1.8
    uptime_fraction: float = 0.7

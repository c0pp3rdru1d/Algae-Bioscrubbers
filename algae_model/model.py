from __future__ import annotations

from .params import ReactorParams

# Import EnergyParams - need to handle the import path
try:
    from ..energy import EnergyParams
except ImportError:
    # Fallback for different import structure
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from energy import EnergyParams

DAYS_PER_YEAR = 365.0

def annual_co2_kg(params: ReactorParams) -> float:
    """
        Compute CO2 removed per year (in kg) for a single reactor.

        Formula:
        C02_kg = (A * P * k * days * uptime) / 1000

        where:
            A = area_m2
            P = productivity_g_m2_day (g/m**2/day)
            k = c02_per_biomass (g C02 / g biomass)
            days = 365 
            uptime = uptime_fraction
        """
        
    grams_c02_per_year = (
            params.area_m2
            * params.productivity_g_m2_day
            * params.c02_per_biomass
            * DAYS_PER_YEAR
            * params.uptime_fraction
        )
    return grams_c02_per_year / 1000.0 # g -> C02_kg

def fleet_co2_tons_per_year(params: ReactorParams, households: int) -> float:
    """
        Compute total CO2 (metric tons per year) for a fleet of identical algae bioreactors.
    """
    return annual_co2_kg(params) * households / 1000.0 # kg -> tons

def percent_of_household_emissions(
    params: ReactorParams,
    household_emissions_tons_per_year: float = 48.0,
) -> float:
    """
    Fraction (%) of an average household's annual CO₂ emissions offset
    by a single reactor, given that household's total emissions.

    Default: ~48 t CO₂ / year (typical US household ballpark).
    """
    reactor_tons = annual_co2_kg(params) / 1000.0
    if household_emissions_tons_per_year <= 0:
        return 0.0
    return 100.0 * reactor_tons / household_emissions_tons_per_year


def annual_co2_kg_with_clean_energy(
    params: ReactorParams,
    energy: EnergyParams,
    extra_co2_per_kwh: float = 0.086,
) -> float:
    """
    Compute CO2 removed per year (in kg) for a single reactor with clean energy enhancement.
    
    This includes the base CO2 capture from photosynthesis plus additional CO2 capture
    from enhanced lighting powered by clean energy.
    
    Args:
        params: Basic reactor parameters
        energy: Clean energy parameters
        extra_co2_per_kwh: Additional CO2 captured (kg) per kWh of lighting energy
    
    Returns:
        Total CO2 captured in kg/year including clean energy enhancement
    """
    # Base CO2 capture from normal operation
    base_co2_kg = annual_co2_kg(params)
    
    # Additional CO2 from clean energy lighting
    lighting_kwh_per_year = energy.clean_kwh_per_year * energy.lighting_fraction
    extra_co2_kg = lighting_kwh_per_year * extra_co2_per_kwh
    
    return base_co2_kg + extra_co2_kg


def fleet_co2_tons_with_clean_energy(
    params: ReactorParams,
    energy: EnergyParams,
    households: int,
    extra_co2_per_kwh: float = 0.086,
) -> float:
    """
    Compute total CO2 (metric tons per year) for a fleet of identical algae bioreactors
    with clean energy enhancement.
    
    Args:
        params: Basic reactor parameters
        energy: Clean energy parameters  
        households: Number of reactors in the fleet
        extra_co2_per_kwh: Additional CO2 captured (kg) per kWh of lighting energy
    
    Returns:
        Total CO2 captured in metric tons/year for the entire fleet
    """
    per_reactor_kg = annual_co2_kg_with_clean_energy(params, energy, extra_co2_per_kwh)
    return per_reactor_kg * households / 1000.0  # kg -> tons

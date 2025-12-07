# fuel.py - Fuel conversion and climate impact calculations
from dataclasses import dataclass


@dataclass
class FuelParams:
    """
    Parameters for converting algal biomass into liquid fuel and estimating
    avoided fossil CO₂ emissions.

    Assumptions (tweak as you like):
      - lipid_fraction:
          Fraction (0–1) of dry biomass that is convertible lipid/oil.
          0.3 = 30% (optimistic but not insane for high-lipid strains).
      - conversion_efficiency:
          Fraction (0–1) of lipids that end up as usable fuel.
          0.8 means 80% of oil ends up as biodiesel/renewable diesel.
      - fuel_density_kg_per_l:
          Density of the produced fuel in kg per liter.
          Biodiesel is ~0.88 kg/L.
      - co2_kg_per_liter_fossil:
          How much CO₂ burning 1 L of fossil diesel emits.
          ~2.6 kg CO₂/L is a common estimate.
      - process_energy_kwh_per_liter:
          How many kWh of energy are needed to process 1 L of fuel
          (extraction, refining). Set to 0 if you don't care yet.
      - process_co2_kg_per_kwh:
          CO₂ intensity of the processing energy (kg CO₂/kWh).
          If powered by wave/solar, this can be ~0.0.
    """
    lipid_fraction: float = 0.30
    conversion_efficiency: float = 0.80
    fuel_density_kg_per_l: float = 0.88
    co2_kg_per_liter_fossil: float = 2.6
    process_energy_kwh_per_liter: float = 0.0
    process_co2_kg_per_kwh: float = 0.0


def biomass_kg_from_co2(co2_kg: float, co2_per_kg_biomass: float = 1.8) -> float:
    """
    Convert fixed CO₂ (kg) to algal dry biomass (kg), using a typical
    ~1.8 kg CO₂ fixed per kg dry biomass.

    biomass_kg = co2_kg / co2_per_kg_biomass
    """
    if co2_per_kg_biomass <= 0:
        return 0.0
    return co2_kg / co2_per_kg_biomass


def fuel_liters_from_biomass(biomass_kg: float, fuel_params: FuelParams) -> float:
    """
    Convert algal biomass (kg) into liters of fuel.
    """
    lipid_fraction = max(0.0, min(1.0, fuel_params.lipid_fraction))
    conversion_eff = max(0.0, min(1.0, fuel_params.conversion_efficiency))

    lipids_kg = biomass_kg * lipid_fraction * conversion_eff
    if fuel_params.fuel_density_kg_per_l <= 0:
        return 0.0

    fuel_liters = lipids_kg / fuel_params.fuel_density_kg_per_l
    return fuel_liters


def avoided_co2_kg_from_fuel(fuel_liters: float, fuel_params: FuelParams) -> float:
    """
    CO₂ avoided by using this algal fuel instead of fossil diesel/jet.

    avoided_CO2 = liters_fuel * co2_kg_per_liter_fossil
    """
    return fuel_liters * fuel_params.co2_kg_per_liter_fossil


def process_emissions_kg_from_fuel(fuel_liters: float, fuel_params: FuelParams) -> float:
    """
    CO₂ emitted by the processing energy for this fuel, if any.
    """
    kwh = fuel_liters * fuel_params.process_energy_kwh_per_liter
    return kwh * fuel_params.process_co2_kg_per_kwh


def fuel_and_climate_effect_for_reactor(
    co2_fixed_kg: float,
    fuel_params: FuelParams,
    co2_per_kg_biomass: float = 1.8,
) -> dict:
    """
    Given how much CO₂ a reactor fixed in a year (kg), compute:

      - biomass_kg: dry algal biomass produced
      - fuel_liters: liters of algal fuel produced (if all biomass is used)
      - avoided_co2_kg: fossil CO₂ avoided by using this fuel
      - process_emissions_kg: CO₂ from processing energy
      - net_climate_effect_kg:
          = co2_fixed_kg + avoided_co2_kg - process_emissions_kg
    """
    biomass_kg = biomass_kg_from_co2(co2_fixed_kg, co2_per_kg_biomass)
    fuel_liters = fuel_liters_from_biomass(biomass_kg, fuel_params)
    avoided_co2_kg = avoided_co2_kg_from_fuel(fuel_liters, fuel_params)
    process_emissions_kg = process_emissions_kg_from_fuel(fuel_liters, fuel_params)

    net_climate_effect_kg = co2_fixed_kg + avoided_co2_kg - process_emissions_kg

    return {
        "co2_fixed_kg": co2_fixed_kg,
        "biomass_kg": biomass_kg,
        "fuel_liters": fuel_liters,
        "avoided_co2_kg": avoided_co2_kg,
        "process_emissions_kg": process_emissions_kg,
        "net_climate_effect_kg": net_climate_effect_kg,
    }


#!/usr/bin/env python3
from __future__ import annotations
from algae_model.fuel import FuelParams, fuel_and_climate_effect_for_reactor
import argparse

from algae_model.model import (
    annual_co2_kg,
    fleet_co2_tons_per_year,
    percent_of_household_emissions,
    annual_co2_kg_with_clean_energy,
    fleet_co2_tons_with_clean_energy,
)
from algae_model.params import ReactorParams
from algae_model.scenarios import SCENARIO_MAP
from energy import EnergyParams


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backyard / Ocean Algae Bio-Engine CO₂ Reduction Model"
    )

    parser.add_argument(
        "--scenario",
        choices=sorted(SCENARIO_MAP.keys()),
        help="Use a predefined reactor scenario (overrides manual params)",
    )

    parser.add_argument(
        "--households",
        type=int,
        default=1,
        help="Number of households / reactors (default: 1)",
    )

    # Reactor parameters
    parser.add_argument(
        "--area-m2",
        type=float,
        help="Reactor area in square meters (m²)",
    )
    parser.add_argument(
        "--productivity",
        type=float,
        help="Biomass productivity in g/m²/day",
    )
    parser.add_argument(
        "--uptime",
        type=float,
        help="Uptime fraction (0.0–1.0, default 0.7 if not using a scenario)",
    )
    parser.add_argument(
        "--co2-per-gram",
        type=float,
        help="CO₂ fixed per gram biomass (g CO₂ / g biomass, default 1.8)",
    )
    parser.add_argument(
        "--household-emissions",
        type=float,
        default=48.0,
        help="Average household annual emissions in tons CO₂ "
             "(default: 48 t/yr for a US household).",
    )

    # Clean energy parameters
    parser.add_argument(
        "--use-clean-energy",
        action="store_true",
        help="Enable clean energy mode (wave/solar/etc powering lighting).",
    )
    parser.add_argument(
        "--clean-kwh-per-year",
        type=float,
        default=0.0,
        help="Clean energy available per reactor per year (kWh).",
    )
    parser.add_argument(
        "--lighting-fraction",
        type=float,
        default=0.0,
        help="Fraction (0–1) of clean kWh used for LEDs (rest assumed for pumps/mixing).",
    )
    parser.add_argument(
        "--extra-co2-per-kwh",
        type=float,
        default=0.086,
        help="Extra CO₂ captured (kg) per kWh used on lighting (default ~0.086).",
    )
        # Fuel / bioenergy mode
    parser.add_argument(
        "--use-fuel",
        action="store_true",
        help="Enable fuel mode: convert biomass into fuel and estimate avoided CO₂.",
    )
    parser.add_argument(
        "--lipid-fraction",
        type=float,
        default=0.30,
        help="Fraction of biomass that is lipid/oil (0–1, default 0.30).",
    )
    parser.add_argument(
        "--fuel-conversion-efficiency",
        type=float,
        default=0.80,
        help="Fraction of lipids converted into usable fuel (0–1, default 0.80).",
    )
    parser.add_argument(
        "--fuel-density-kg-per-l",
        type=float,
        default=0.88,
        help="Fuel density in kg/L (default 0.88 for biodiesel).",
    )
    parser.add_argument(
        "--fossil-co2-per-liter",
        type=float,
        default=2.6,
        help="CO₂ emitted by burning 1 L of fossil diesel (kg CO₂/L, default 2.6).",
    )
    parser.add_argument(
        "--process-energy-kwh-per-liter",
        type=float,
        default=0.0,
        help="kWh of processing energy needed per liter of algal fuel (default 0.0).",
    )
    parser.add_argument(
        "--process-co2-kg-per-kwh",
        type=float,
        default=0.0,
        help="CO₂ intensity of processing energy (kg CO₂/kWh, default 0.0 for clean power).",
    )

    return parser.parse_args()


def build_params_from_args(args: argparse.Namespace) -> ReactorParams:
    if args.scenario:
        base = SCENARIO_MAP[args.scenario]()
        area_m2 = args.area_m2 if args.area_m2 is not None else base.area_m2
        productivity = (
            args.productivity
            if args.productivity is not None
            else base.productivity_g_m2_day
        )
        uptime = args.uptime if args.uptime is not None else base.uptime_fraction
        co2_per_gram = (
            args.co2_per_gram
            if args.co2_per_gram is not None
            else base.c02_per_biomass
        )
    else:
        area_m2 = args.area_m2 if args.area_m2 is not None else 4.0
        productivity = args.productivity if args.productivity is not None else 20.0
        uptime = args.uptime if args.uptime is not None else 0.7
        co2_per_gram = args.co2_per_gram if args.co2_per_gram is not None else 1.8

    return ReactorParams(
        area_m2=area_m2,
        productivity_g_m2_day=productivity,
        c02_per_biomass=co2_per_gram,
        uptime_fraction=uptime,
    )


def build_energy_from_args(args: argparse.Namespace) -> EnergyParams:
    return EnergyParams(
        clean_kwh_per_year=args.clean_kwh_per_year,
        lighting_fraction=args.lighting_fraction,
    )

def build_fuel_params_from_args(args: argparse.Namespace) -> FuelParams:
    return FuelParams(
        lipid_fraction=args.lipid_fraction,
        conversion_efficiency=args.fuel_conversion_efficiency,
        fuel_density_kg_per_l=args.fuel_density_kg_per_l,
        co2_kg_per_liter_fossil=args.fossil_co2_per_literal if False else args.fossil_co2_per_liter,  # we'll fix below
        process_energy_kwh_per_liter=args.process_energy_kwh_per_literal if False else args.process_energy_kwh_per_liter,
        process_co2_kg_per_kwh=args.process_co2_kg_per_kwh,
    )


def pretty_print_results_base(
    params: ReactorParams,
    households: int,
    household_emissions_tons: float,
) -> None:
    per_reactor_kg = annual_co2_kg(params)
    total_tons = fleet_co2_tons_per_year(params, households)
    percent_offset = percent_of_household_emissions(params, household_emissions_tons)

    print("=== Backyard / Ocean Algae Bio-Engine CO₂ Model ===")
    print()
    print(f"Reactor parameters:")
    print(f"  Area:              {params.area_m2:.2f} m²")
    print(f"  Productivity:      {params.productivity_g_m2_day:.1f} g/m²/day")
    print(f"  CO₂ per biomass:   {params.c02_per_biomass:.2f} g CO₂ / g biomass")
    print(f"  Uptime:            {params.uptime_fraction * 100:.1f} %")
    print()
    print(f"Sunlight-only (no clean-energy lighting):")
    print(f"  Per reactor:       {per_reactor_kg:.2f} kg CO₂ / year")
    print(f"  Offset vs household emissions "
          f"({household_emissions_tons:.1f} t/yr): "
          f"{percent_offset:.3f} %")
    print(f"  Fleet ({households} reactors): {total_tons:.3f} tons CO₂ / year")
    print()


def pretty_print_results_with_clean_energy(
    params: ReactorParams,
    energy: EnergyParams,
    households: int,
    household_emissions_tons: float,
    extra_co2_per_kwh: float,
) -> None:
    base_per_reactor_kg = annual_co2_kg(params)
    boosted_per_reactor_kg = annual_co2_kg_with_clean_energy(
        params, energy, extra_co2_per_kwh=extra_co2_per_kwh
    )
    base_fleet_tons = fleet_co2_tons_per_year(params, households)
    boosted_fleet_tons = fleet_co2_tons_with_clean_energy(
        params, energy, households, extra_co2_per_kwh=extra_co2_per_kwh
    )

    extra_per_reactor = boosted_per_reactor_kg - base_per_reactor_kg
    extra_fleet = boosted_fleet_tons - base_fleet_tons

    print("=== Clean Energy Mode (Wave/Solar-Powered) ===")
    print()
    print(f"Clean energy per reactor: {energy.clean_kwh_per_year:.1f} kWh/year")
    print(f"Lighting fraction:        {energy.lighting_fraction * 100:.1f} %")
    print(f"Extra CO₂ per kWh (lighting): {extra_co2_per_kwh:.3f} kg/kWh")
    print()
    print("Per reactor:")
    print(f"  Base (sunlight only):  {base_per_reactor_kg:.2f} kg CO₂ / year")
    print(f"  With clean energy:     {boosted_per_reactor_kg:.2f} kg CO₂ / year")
    print(f"  Extra from lighting:   {extra_per_reactor:.2f} kg CO₂ / year")
    print()
    print(f"Fleet (reactors = {households}):")
    print(f"  Base:                  {base_fleet_tons:.3f} tons CO₂ / year")
    print(f"  With clean energy:     {boosted_fleet_tons:.3f} tons CO₂ / year")
    print(f"  Extra from lighting:   {extra_fleet:.3f} tons CO₂ / year")
    print()


def pretty_print_fuel_results(
    per_reactor_co2_kg: float,
    households: int,
    fuel_params: FuelParams,
) -> None:
    result = fuel_and_climate_effect_for_reactor(
        co2_fixed_kg=per_reactor_co2_kg,
        fuel_params=fuel_params,
    )

    fleet_multiplier = households
    print("=== Fuel Mode: Biomass → Fuel → Avoided CO₂ ===")
    print()
    print("Fuel parameters:")
    print(f"  Lipid fraction:            {fuel_params.lipid_fraction * 100:.1f} %")
    print(f"  Conversion efficiency:     {fuel_params.conversion_efficiency * 100:.1f} %")
    print(f"  Fuel density:              {fuel_params.fuel_density_kg_per_l:.2f} kg/L")
    print(f"  Fossil CO₂ per liter:      {fuel_params.co2_kg_per_liter_fossil:.2f} kg CO₂/L")
    print(f"  Process energy per liter:  {fuel_params.process_energy_kwh_per_liter:.2f} kWh/L")
    print(f"  Process CO₂ intensity:     {fuel_params.process_co2_kg_per_kwh:.3f} kg CO₂/kWh")
    print()
    print("Per reactor (per year):")
    print(f"  CO₂ fixed:                 {result['co2_fixed_kg']:.2f} kg")
    print(f"  Biomass produced:          {result['biomass_kg']:.2f} kg")
    print(f"  Fuel produced:             {result['fuel_liters']:.2f} L")
    print(f"  Avoided fossil CO₂:        {result['avoided_co2_kg']:.2f} kg")
    print(f"  Processing emissions:      {result['process_emissions_kg']:.2f} kg")
    print(f"  Net climate effect:        {result['net_climate_effect_kg']:.2f} kg")
    print()
    print(f"Fleet (reactors = {households}):")
    print(f"  Fuel produced:             {result['fuel_liters'] * fleet_multiplier:.2f} L/year")
    print(f"  Avoided fossil CO₂:        {result['avoided_co2_kg'] * fleet_multiplier / 1000.0:.3f} t/year")
    print(f"  Processing emissions:      {result['process_emissions_kg'] * fleet_multiplier / 1000.0:.3f} t/year")
    print(f"  Net climate effect:        {result['net_climate_effect_kg'] * fleet_multiplier / 1000.0:.3f} t/year")
    print()




def main() -> None:
    args = parse_args()
    params = build_params_from_args(args)

    # Base (sun-only) printout
    pretty_print_results_base(
        params=params,
        households=args.households,
        household_emissions_tons=args.household_emissions,
    )

    # Decide which CO₂ number is "actual" for fuel calculations:
    per_reactor_co2_kg = annual_co2_kg(params)

    if args.use_clean_energy:
        energy = build_energy_from_args(args)
        pretty_print_results_with_clean_energy(
            params=params,
            energy=energy,
            households=args.households,
            household_emissions_tons=args.household_emissions,
            extra_co2_per_kwh=args.extra_co2_per_kwh,
        )
        # If clean energy is used, fuel comes from boosted capture:
        per_reactor_co2_kg = annual_co2_kg_with_clean_energy(
            params=params,
            energy=energy,
            extra_co2_per_kwh=args.extra_co2_per_kwh,
        )

    if args.use_fuel:
        fuel_params = build_fuel_params_from_args(args)
        pretty_print_fuel_results(
            per_reactor_co2_kg=per_reactor_co2_kg,
            households=args.households,
            fuel_params=fuel_params,
        )



if __name__ == "__main__":
    main()


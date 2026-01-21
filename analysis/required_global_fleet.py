"""Analysis to determine the required size of the global fleet."""

import camia_engine as engine
from camia_model.units import day, year

import aviation
from aviation.units import aircraft, journey, passenger

# from aviation import _engine as engine
# Alternative import if aviation._engine is directly accessible

# Constants
days_per_year = 365.0 * day / year
seats_per_aircraft = 200.0 * passenger / aircraft
flights_per_aircraft_per_day = 3.0 * journey / (aircraft * day)
passengers_per_year = 5_000_000_000.0 * passenger / year

inputs = {
    "passengers_per_year": passengers_per_year,
    "days_per_year": days_per_year,
    "seats_per_aircraft": seats_per_aircraft,
    "flights_per_aircraft_per_day": flights_per_aircraft_per_day,
}
output = "required_global_fleet"

systems_model = engine.SystemsModel(aviation.transforms)
required_global_fleet = systems_model.evaluate(inputs, output)

print("Required Global Fleet:", round(required_global_fleet))

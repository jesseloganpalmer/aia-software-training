"""Analysis to determine the number of passengers per day globally."""

import camia_engine as engine
from camia_model.units import day, year

import aviation
from aviation.units import passenger

# from aviation import _engine as engine
# Alternative import if aviation._engine is directly accessible

# Constants
days_per_year = 365.0 * day / year
passengers_per_year = 5_000_000_000.0 * passenger / year

inputs = {
    "days_per_year": days_per_year,
    "passengers_per_year": passengers_per_year,
}
output = "passengers_per_day"

systems_model = engine.SystemsModel(aviation.transforms)
passengers_per_day = systems_model.evaluate(inputs, output)
print("Passenger per day:", round(passengers_per_day))

"""Modelling of the global fleet based on average passenger and aircraft data."""

import camia_model as model

# from aviation import _model as model
# Alternative import if aviation._model is directly accessible


# Global passengers per day
@model.transform
def passengers_per_day(passengers_per_year: float, days_per_year: float) -> float:
    """The number of passengers per day globally.

    Args:
      passengers_per_year: The number of passengers flying per year globally.
      days_per_year: The number of days in the modelled year.

    """
    return passengers_per_year / days_per_year


# Global fleet
@model.transform
def required_global_fleet(
    passengers_per_day: float, seats_per_aircraft: float, flights_per_aircraft_per_day: float
) -> float:
    """The size of the required global fleet.

    Args:
      passengers_per_day: The number of passengers flying per day globally.
      seats_per_aircraft: The average number of seats on a commercial aircraft.
      flights_per_aircraft_per_day: The average number of flights a commercial aircraft
      makes on average per day.

    """
    return passengers_per_day / (seats_per_aircraft * flights_per_aircraft_per_day)

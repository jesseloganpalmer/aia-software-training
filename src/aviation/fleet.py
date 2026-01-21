"""Modelling of the global fleet based on average passenger and aircraft data."""

__all__ = ("passengers_per_day", "required_global_fleet")

import typing

import camia_model as model
from camia_model.units import Quantity, day, year

from aviation.units import aircraft, journey, passenger

# from aviation import _model as model
# Alternative import if aviation._model is directly accessible


# Global passengers per day
@model.transform
def passengers_per_day(
    passengers_per_year: typing.Annotated[Quantity, passenger / year],
    days_per_year: typing.Annotated[Quantity, day / year],
) -> typing.Annotated[Quantity, passenger / day]:
    """The number of passengers per day globally.

    Args:
      passengers_per_year: The number of passengers flying per year globally.
      days_per_year: The number of days in the modelled year.

    """
    return passengers_per_year / days_per_year


# Global fleet
@model.transform
def required_global_fleet(
    passengers_per_day: typing.Annotated[Quantity, passenger / day],
    seats_per_aircraft: typing.Annotated[Quantity, passenger / aircraft],
    flights_per_aircraft_per_day: typing.Annotated[Quantity, journey / (aircraft * day)],
) -> typing.Annotated[Quantity, aircraft]:
    """The size of the required global fleet.

    Args:
      passengers_per_day: The number of passengers flying per day globally.
      seats_per_aircraft: The average number of seats on a commercial aircraft.
      flights_per_aircraft_per_day: The average number of flights a commercial aircraft
      makes on average per day.

    """
    aircraft_per_journey = 1.0 * aircraft / journey
    return passengers_per_day / (
        seats_per_aircraft * flights_per_aircraft_per_day * aircraft_per_journey
    )

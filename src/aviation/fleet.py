"""Modelling of the global fleet based on average passenger and aircraft data."""


# Global gassengers per day
def passengers_per_day(passengers_per_plane, days_per_year):
    """The number of passengers per day globally."""
    return passengers_per_plane / days_per_year


# Global fleet
def required_global_fleet(passengers_per_day, seats_per_aircraft, flights_per_aircraft_per_day):
    """The size of the required global fleet."""
    return passengers_per_day / (seats_per_aircraft * flights_per_aircraft_per_day)

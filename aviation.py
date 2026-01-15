# Global gassengers per day
def passengers_per_day(passengers_per_plane, days_per_year):
    return passengers_per_plane / days_per_year


# Global fleet
def required_global_fleet(
    passengers_per_day, seats_per_aircraft, flights_per_aircraft_per_day
):
    return passengers_per_day / (seats_per_aircraft * flights_per_aircraft_per_day)


print(f"{required_global_fleet=}")

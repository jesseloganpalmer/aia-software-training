"""Analysis to determine the number of passengers per day globally."""

import aviation

# Constants
days_per_year = 365.0
passengers_per_plane = 5_000_000_000.0
seats_per_aircraft = 150
flights_per_aircraft_per_day = 2.0

passengers_per_day = aviation.passengers_per_day
print(f"{passengers_per_day=}")

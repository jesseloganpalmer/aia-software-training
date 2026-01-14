# Constants
days_per_year = 365.0
passengers_per_plane = 5_000_000_000.0
seats_per_aircraft = 150
flights_per_aircraft_per_day = 2.0

# Global gassengers per day
passengers_per_day = passengers_per_plane / days_per_year

# Global fleet
required_global_fleet = passengers_per_day / (
    seats_per_aircraft * flights_per_aircraft_per_day
)

print(f"{required_global_fleet=}")

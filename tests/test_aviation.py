import pytest

from aviation.fleet import passengers_per_day, required_global_fleet


@pytest.mark.parametrize(
    ("passengers_per_year", "days_per_year", "expected_passengers_per_day"),
    (
        (365_000_000.0, 365.0, 1_000_000.0),
        (365_250_000.0, 365.25, 1_000_000.0),
        (366_000_000.0, 366.0, 1_000_000.0),
        (5_000_000_000.0, 365.0, 13_698_630.0),
    ),
)
def test_passengers_per_day(
    passengers_per_year: float, days_per_year: float, expected_passengers_per_day: float
) -> None:
    result = passengers_per_day(passengers_per_year, days_per_year)
    assert result == pytest.approx(expected_passengers_per_day)


def test_required_global_fleet() -> None:
    days_per_year = 365.0
    passengers_per_year = 5_000_000_000.0
    seats_per_aircraft = 160.0
    flights_per_aircraft_per_day = 2.5

    expected_required_global_fleet = 25_000.0

    result = required_global_fleet(
        passengers_per_day(passengers_per_year, days_per_year),
        seats_per_aircraft,
        flights_per_aircraft_per_day,
    )
    assert result == pytest.approx(expected_required_global_fleet, abs=10_000.0)

"""Creates visual representation of Required Global Fleet analysis."""

from typing import Any

import camia_engine as engine
import numpy as np
import plotly.graph_objects as go
from camia_model.units import day, year

import aviation
from aviation.units import aircraft, journey, passenger

days_per_year = 365.0 * day / year

flights_per_aircraft_per_day = 3.0 * journey / (aircraft * day)

# seats_per_aircraft = 200.0 * passenger / aircraft
seats_per_aircraft_raw = np.arange(50.0, 1000.0, 50.0)
seats_per_aircraft: list[Any] = [s * passenger / aircraft for s in seats_per_aircraft_raw]

passengers_per_year_raw = np.arange(0.0, 10_500_000_000.0, 500_000_000.0)
passengers_per_year: list[Any] = [p * passenger / year for p in passengers_per_year_raw]

inputs = {
    "passengers_per_year": passengers_per_year,
    "days_per_year": days_per_year,
    "seats_per_aircraft": seats_per_aircraft,
    "flights_per_aircraft_per_day": flights_per_aircraft_per_day,
}
output = "required_global_fleet"

systems_model = engine.SystemsModel(aviation.transforms)
required_global_fleet = systems_model.evaluate(inputs, output)
print(required_global_fleet)

# Extract numeric values from the 2D array - select first row of seats_per_aircraft (50 passengers)
required_global_fleet_values = [q.value for q in required_global_fleet.values[0]]
passengers_per_year_values = [q.value for q in passengers_per_year]

fig = go.Figure(
    data=go.Scatter(
        x=passengers_per_year_values,
        y=required_global_fleet_values,
        mode="lines+markers",
        name="Passengers per day",
        marker=dict(size=10, line=dict(width=1)),  # noqa: C408
        hovertemplate="<b>Passengers per year:</b> %{x}<br><b>Passengers per day:</b> %{y}<extra></extra>",
    )
)
fig.update_layout(
    xaxis_title="Passengers per year",
    yaxis_title="Required Global Fleet",
    title="Global Fleet of Aircraft",
    font=dict(size=14),  # noqa: C408
    title_font_size=20,
    hoverlabel=dict(font_size=14),  # noqa: C408
)
fig.write_html("docs/assets/plot_fleet.html")

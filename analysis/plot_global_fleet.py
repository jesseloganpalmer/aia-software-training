"""Creates visual representation of Required Global Fleet analysis."""

from typing import Any

import camia_engine as engine
import numpy as np
import plotly.graph_objects as go
from camia_model.units import day, year

import aviation
from aviation.units import aircraft, journey, passenger

days_per_year = 365.0 * day / year


flights_per_aircraft_per_day_raw = np.arange(1.0, 4.0, 1.0)
flights_per_aircraft_per_day: list[Any] = [
    f * journey / (aircraft * day) for f in flights_per_aircraft_per_day_raw
]

# seats_per_aircraft = 200.0 * passenger / aircraft
seats_per_aircraft_raw = np.arange(50.0, 550.0, 50.0)
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

inputs = {
    "days_per_year": days_per_year,
    "passengers_per_year": passengers_per_year,
}
output = "passengers_per_day"

systems_model = engine.SystemsModel(aviation.transforms)
passengers_per_day = systems_model.evaluate(inputs, output)


# Extract numeric values from Quantity objects
passengers_per_day_values = [q.value for q in passengers_per_day.values]


# Extract numeric values from passengers_per_year for x-axis
passengers_per_year_values = [q.value for q in passengers_per_year]
seats_per_aircraft_values = [q.value for q in seats_per_aircraft]
flights_per_aircraft_per_day_values = [q.value for q in flights_per_aircraft_per_day]

# Create traces for each combination of seats_per_aircraft and flights_per_aircraft_per_day
# Defaults show the smallest values (50 seats, 1 flight per day)
DEFAULT_SEATS_INDEX = 0
DEFAULT_FLIGHTS_INDEX = 0
fig = go.Figure()
for f_idx, flights_value in enumerate(flights_per_aircraft_per_day_values):
    for s_idx, _seats_value in enumerate(seats_per_aircraft_values):
        # Array is indexed as [passengers_per_day, seats_per_aircraft, flights_per_aircraft_per_day]
        fleet_values = [q.value for q in required_global_fleet.values[:, s_idx, f_idx]]
        # Show all traces for default seats index, hide others
        is_visible = s_idx == DEFAULT_SEATS_INDEX
        fig.add_trace(
            go.Scatter(
                x=passengers_per_day_values,
                y=fleet_values,
                mode="lines+markers",
                name=f"Flights: {flights_value:.0f}",
                marker={"size": 8, "line": {"width": 1}},
                hovertemplate="<b>Passengers per day:</b> %{x:.2e}<br><b>Required Fleet:</b> %{y:.0f}<extra></extra>",
                visible=is_visible,
            )
        )

# Add vertical line showing current passenger levels (approximately 5B passengers/year = 13.7M/day)
current_passengers_per_day = 5_000_000_000 / 365.0  # ~13.7 million per day
fig.add_vline(
    x=current_passengers_per_day,
    line_dash="dash",
    line_color="red",
    line_width=2,
    annotation_text="Current Scenario (~13.7M/day)",
    annotation_position="top right",
    annotation=dict(font_size=12, font_color="red"),  # noqa: C408
)

# Create slider steps for seats_per_aircraft
# Each step shows all flights for that seat value
steps: list[Any] = []
for s_idx, seats_value in enumerate(seats_per_aircraft_values):
    # Show all traces for this seats index (all flights)
    visible_list: list[bool] = [
        (s_idx_check == s_idx)
        for f_idx_check in range(len(flights_per_aircraft_per_day_values))
        for s_idx_check in range(len(seats_per_aircraft_values))
    ]
    step = dict(  # noqa: C408
        method="update",
        args=[
            {"visible": visible_list},
            {"title": {"text": "Global Fleet Required"}},
        ],
        label=f"{seats_value:.0f}",
    )
    steps.append(step)

sliders = [
    dict(  # noqa: C408
        active=DEFAULT_SEATS_INDEX,
        yanchor="bottom",
        y=-0.25,
        xanchor="left",
        x=0.0,
        len=1.0,
        transition=dict(duration=300),  # noqa: C408
        pad=dict(b=10, t=50),  # noqa: C408
        font=dict(size=10),  # noqa: C408
        ticklen=5,
        currentvalue=dict(  # noqa: C408
            prefix="Seats per Aircraft: ",
            visible=True,
            xanchor="right",
            font=dict(size=10),  # noqa: C408
        ),
        steps=steps,
    )
]

fig.update_layout(
    sliders=sliders,
    xaxis_title="Passengers per day",
    yaxis_title="Required Global Fleet",
    xaxis=dict(range=[0, 28_000_000], dtick=2_000_000),  # noqa: C408
    yaxis=dict(range=[0, 600000], dtick=50000),  # noqa: C408
    title="Global Fleet Required",
    font=dict(size=14),  # noqa: C408
    title_font_size=20,
    hoverlabel=dict(font_size=14),  # noqa: C408
    height=700,
)
fig.write_html("docs/assets/plot_fleet.html")

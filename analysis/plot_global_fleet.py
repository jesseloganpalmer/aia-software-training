"""Creates visual representation of Required Global Fleet analysis."""

from typing import Any

import camia_engine as engine
import numpy as np
import plotly.graph_objects as go
from camia_model.units import day, year

import aviation
from aviation.units import aircraft, journey, passenger

days_per_year = 365.0 * day / year

# flights_per_aircraft_per_day = 3.0 * journey / (aircraft * day)
flights_per_aircraft_per_day_raw = np.arange(1.0, 11.0, 1.0)
flights_per_aircraft_per_day: list[Any] = [
    f * journey / (aircraft * day) for f in flights_per_aircraft_per_day_raw
]

# seats_per_aircraft = 200.0 * passenger / aircraft
seats_per_aircraft_raw = np.arange(50.0, 1050.0, 50.0)
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


# Extract numeric values from passengers_per_year for x-axis
passengers_per_year_values = [q.value for q in passengers_per_year]
seats_per_aircraft_values = [q.value for q in seats_per_aircraft]
flights_per_aircraft_per_day_values = [q.value for q in flights_per_aircraft_per_day]

# Create traces for each combination of seats_per_aircraft and flights_per_aircraft_per_day
DEFAULT_SEATS_INDEX = 3  # 200 seats per aircraft
DEFAULT_FLIGHTS_INDEX = 2  # 3 flights per aircraft per day
fig = go.Figure()
for f_idx, flights_value in enumerate(flights_per_aircraft_per_day_values):
    for s_idx, seats_value in enumerate(seats_per_aircraft_values):
        # Array is indexed as [passengers_per_year, seats_per_aircraft, flights_per_aircraft_per_day]
        fleet_values = [q.value for q in required_global_fleet.values[:, s_idx, f_idx]]
        # Show 200 seats and 3 flights by default
        is_visible = s_idx == DEFAULT_SEATS_INDEX and f_idx == DEFAULT_FLIGHTS_INDEX
        fig.add_trace(
            go.Scatter(
                x=passengers_per_year_values,
                y=fleet_values,
                mode="lines+markers",
                name=f"Seats: {seats_value:.0f}, Flights: {flights_value:.0f}",
                marker={"size": 8, "line": {"width": 1}},
                hovertemplate="<b>Passengers per year:</b> %{x:.2e}<br><b>Required Fleet:</b> %{y:.0f}<extra></extra>",
                visible=is_visible,
            )
        )

# Create slider steps for seats_per_aircraft
steps: list[Any] = []
for s_idx, seats_value in enumerate(seats_per_aircraft_values):
    # For seats slider: show only the trace for this seats index and default flights index
    visible_list: list[bool] = [
        (f_idx_check == DEFAULT_FLIGHTS_INDEX and s_idx_check == s_idx)
        for f_idx_check in range(len(flights_per_aircraft_per_day_values))
        for s_idx_check in range(len(seats_per_aircraft_values))
    ]
    step = dict(  # noqa: C408
        method="update",
        args=[
            {"visible": visible_list},
            {"title": f"Global Fleet Required (Seats per Aircraft: {seats_value:.0f})"},
        ],
        label=f"{seats_value:.0f}",
    )
    steps.append(step)

sliders = [
    dict(  # noqa: C408
        active=0,
        yanchor="top",
        y=0,
        xanchor="left",
        x=0.1,
        len=0.75,
        transition=dict(duration=300),  # noqa: C408
        pad=dict(b=10, t=50),  # noqa: C408
        currentvalue=dict(  # noqa: C408
            prefix="Seats per Aircraft: ",
            visible=True,
            xanchor="right",
            font=dict(size=16),  # noqa: C408
        ),
        steps=steps,
    )
]

# Create slider steps for flights_per_aircraft_per_day
flights_steps: list[Any] = []
for f_idx, flights_value in enumerate(flights_per_aircraft_per_day_values):
    # For flights slider: show only the trace for this flights index and default seats index
    flights_visible: list[bool] = [
        (f_idx_check == f_idx and s_idx_check == DEFAULT_SEATS_INDEX)
        for f_idx_check in range(len(flights_per_aircraft_per_day_values))
        for s_idx_check in range(len(seats_per_aircraft_values))
    ]
    step = dict(  # noqa: C408
        method="update",
        args=[
            {"visible": flights_visible},
            {"title": f"Global Fleet Required (Flights per Aircraft per Day: {flights_value:.0f})"},
        ],
        label=f"{flights_value:.0f}",
    )
    flights_steps.append(step)

sliders.append(
    dict(  # noqa: C408
        active=0,
        yanchor="bottom",
        y=-0.15,
        xanchor="left",
        x=0.1,
        len=0.75,
        transition=dict(duration=300),  # noqa: C408
        pad=dict(b=10, t=50),  # noqa: C408
        currentvalue=dict(  # noqa: C408
            prefix="Flights per Aircraft per Day: ",
            visible=True,
            xanchor="right",
            font=dict(size=16),  # noqa: C408
        ),
        steps=flights_steps,
    )
)

fig.update_layout(
    sliders=sliders,
    xaxis_title="Passengers per year",
    yaxis_title="Required Global Fleet",
    yaxis=dict(range=[0, 200000]),  # noqa: C408
    title="Global Fleet Required (Seats per Aircraft: 50)",
    font=dict(size=14),  # noqa: C408
    title_font_size=20,
    hoverlabel=dict(font_size=14),  # noqa: C408
    height=700,
)
fig.write_html("docs/assets/plot_fleet.html")

"""Creates visual representation of Passengers per Day analysis."""

from typing import Any

import camia_engine as engine
import numpy as np
import plotly.graph_objects as go
from camia_model.units import day, year

import aviation
from aviation.units import passenger

# Constants
days_per_year = 365.0 * day / year

# Inputs
passengers_per_year_raw = np.arange(0.0, 10_500_000_000.0, 500_000_000.0)
passengers_per_year: list[Any] = [p * passenger / year for p in passengers_per_year_raw]

inputs = {
    "days_per_year": days_per_year,
    "passengers_per_year": passengers_per_year,
}
output = "passengers_per_day"

systems_model = engine.SystemsModel(aviation.transforms)
passengers_per_day = systems_model.evaluate(inputs, output)


# Extract numeric values from Quantity objects
passengers_per_day_values = [q.value for q in passengers_per_day.values]
passengers_per_year_values = [q.value for q in passengers_per_year]

fig = go.Figure(
    data=go.Scatter(
        x=passengers_per_year_values,
        y=passengers_per_day_values,
        mode="lines+markers",
        name="Passengers per day",
        marker=dict(size=10, line=dict(width=1)),  # noqa: C408
        hovertemplate="<b>Passengers per year:</b> %{x}<br><b>Passengers per day:</b> %{y}<extra></extra>",
    )
)
fig.update_layout(
    xaxis_title="Passengers per year",
    yaxis_title="Passengers per day",
    title="Global Passengers",
    font=dict(size=14),  # noqa: C408
    title_font_size=20,
    hoverlabel=dict(font_size=14),  # noqa: C408
)
fig.write_html("docs/assets/plot_passengers.html")

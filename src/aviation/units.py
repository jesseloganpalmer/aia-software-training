"""Additional units to support accurate unit annotations of transforms."""

__all__ = ("aircraft", "journey", "passenger")

from camia_model.units import DIMENSIONLESS, Unit

aircraft = Unit.new_named("aircraft", relation=DIMENSIONLESS)
journey = Unit.new_named("journey", relation=DIMENSIONLESS)
passenger = Unit.new_named("passenger", relation=DIMENSIONLESS)

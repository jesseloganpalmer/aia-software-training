"""Additional units to support accurate unit annotations of transforms."""

__all__ = ("aircraft", "journey", "passenger")

import camia_model as model
import camia_model.units

aircraft = model.units.Unit.new_named("aircraft", relation=model.units.DIMENSIONLESS)
journey = model.units.Unit.new_named("journey", relation=model.units.DIMENSIONLESS)
passenger = model.units.Unit.new_named("passenger", relation=model.units.DIMENSIONLESS)

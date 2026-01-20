"""A simple model of global aviation."""

__all__ = ("passengers_per_day", "required_global_fleet", "transforms")

from aviation.fleet import passengers_per_day, required_global_fleet

transforms = (passengers_per_day, required_global_fleet)

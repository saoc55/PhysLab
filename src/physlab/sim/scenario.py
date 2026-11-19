from __future__ import annotations
from physlab.physics.world import World
from physlab.sim.parameters import Parameter
from abc import ABC, abstractmethod

class Scenario(ABC):
    
    name:str = ""
    description:str = ""

    @abstractmethod
    def parameters(self) -> list[Parameter]:
        """Every adjustable input of this scenario, as Parameter objects. Same list, same order on every call."""

    @abstractmethod
    def build(self, values: dict[str, float]) -> World:
        """A new World at t = 0, built from values (one number per Parameter key). Never reuses an old world."""

    def default_values(self) -> dict[str, float]:
        return {p.key: p.default for p in self.parameters()}

    def is_finished(self, world:World) -> bool:
        return False

    def view_bounds(self, values: dict[str, float]) -> tuple[float, float, float, float]:
        return (-1,-1,20,12)

    def readouts(self, world:World) -> list[tuple[str, str]]:
        return []



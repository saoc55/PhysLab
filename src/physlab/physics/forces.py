# REVIEW 2 (Claude, 2026-10-12). Nearly done: one physics bug (drag sign), one leftover in force_on, two small spec points.
from __future__ import annotations
from physlab.core.vector2d import Vector2D
from physlab.core.constants import STANDARD_GRAVITY, AIR_DENSITY, SPHERE_DRAG_COEFFICIENT
from physlab.physics.body import Body
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from physlab.physics.world import World

class ForceGenerator(ABC):
    def __init__(self, label: str) -> None:
        self.label = label
        self.enabled = True

    @abstractmethod
    def apply(self, world: World) -> None:
        """Add this generator's forces to the bodies it affects."""

    
    def potential_energy(self, body: Body) -> float:
        return 0.0


class BodyForce(ForceGenerator):
    def apply(self, world) -> None:

        for body in world.bodies:
            body.add_force(self.label, self.force_on(body))
    
    @abstractmethod
    def force_on(self, body: Body) -> Vector2D:
        """Force on one body in N."""


class UniformGravity(BodyForce):
    def __init__(self, g: float = STANDARD_GRAVITY) -> None:
        super().__init__("weight")

        if g < 0:
            raise ValueError("g must not be negative")

        self.g = g

    def force_on(self, body: Body) -> Vector2D:
        return Vector2D(0, -body.mass * self.g)

    def potential_energy(self, body) -> float:
        return body.mass * self.g * body.position.y

class QuadraticDrag(BodyForce):
    def __init__(self, area:float, rho:float = AIR_DENSITY, cd: float = SPHERE_DRAG_COEFFICIENT) -> None:
        super().__init__("drag")

        if area <= 0:
            raise ValueError("Area must be larger than zero")
        if rho < 0:
            raise ValueError("Rho must be larger or equal to zero")
        if cd < 0:
            raise ValueError("cd must be larger or equal to zero")
        
        self.area = area #m2
        self.rho = rho #kg/m3
        self.cd = cd 

    def force_on(self, body: Body) -> Vector2D:
        if body.velocity.is_zero():
            return Vector2D.zero()
        
        return -1 * (0.5 * self.rho * self.cd * self.area * body.velocity.magnitude()) * body.velocity
        
        

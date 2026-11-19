"""AppliedForce, Body. Spec: doc sections 5.3, 5.4, ticket P1-03."""
from __future__ import annotations
from dataclasses import dataclass, field
from physlab.core.vector2d import Vector2D


@dataclass(frozen=True)
class AppliedForce:
    label: str
    vector: Vector2D

@dataclass
class Body:
    
    name: str
    mass: float
    position: Vector2D
    velocity: Vector2D = field(default_factory = Vector2D.zero)
    radius: float = 0.1
    acceleration: Vector2D = field(default_factory = Vector2D.zero)
    _forces: list[AppliedForce] = field(default_factory=list, repr=False, init=False)
               


    def __post_init__(self) -> None:
        
            if not self.name.strip():
                raise ValueError("Name must not be empty")
            if self.mass <= 0:
                raise ValueError("Mass must be larger than zero")
            if self.radius <= 0:
                raise ValueError("radius must be larger than zero")

    @property
    def forces(self) -> tuple[AppliedForce, ...]:
        return tuple(self._forces)
    
    def add_force(self, label: str, vector: Vector2D) -> None:
        new_force = AppliedForce(label, vector)
        self._forces.append(new_force)

    def net_force(self) -> Vector2D:
        net_force = Vector2D.zero()

        for force in self._forces:
            net_force += force.vector
        return net_force

    def clear_forces(self)-> None:
        self._forces.clear()

    def kinetic_energy(self) -> float:
        return self.mass * 0.5 * self.velocity.magnitude_squared()

        



        

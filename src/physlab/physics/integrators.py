from __future__ import annotations
from abc import ABC, abstractmethod
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body



class Integrator(ABC):
    name = ""

    @abstractmethod
    def step(self, body:Body, dt:float) -> None:
        """every integrator must have a step"""
        


class ExplicitEuler(Integrator):
    name = "Explicit Euler"

    def step(self, body: Body, dt:float) -> None:
        body.acceleration = body.net_force() / body.mass
        body.position += body.velocity * dt
        body.velocity += body.acceleration * dt

class SemiImplicitEuler(Integrator):
    name = "Semi Implicit Euler"

    def step(self, body:Body, dt:float) -> None:

        body.acceleration = body.net_force() / body.mass
        body.velocity += body.acceleration * dt
        body.position += body.velocity * dt

        
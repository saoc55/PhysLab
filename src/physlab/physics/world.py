from __future__ import annotations
from physlab.physics.body import Body
from physlab.physics.forces import ForceGenerator
from physlab.physics.integrators import Integrator, SemiImplicitEuler



class World():

    def __init__(self, integrator:Integrator | None = None):
        if integrator is None:
            self.integrator = SemiImplicitEuler()
        else:
            self.integrator = integrator

        self._generators:list[ForceGenerator] = list()
        self._bodies:list[Body] = list()
        self.time = 0.0

    @property
    def bodies(self) -> tuple[Body, ...]:
        return tuple(self._bodies)

    @property
    def generators(self) -> tuple[ForceGenerator, ...]:
        return tuple(self._generators)

#--------------------------------------------------Methods---------------------------------------------------
    
    def add_body(self, body: Body) -> Body:
        for existing in self._bodies:
            if body.name == existing.name:
                raise ValueError("This name already exists")
        self._bodies.append(body)
        return body

    def get_body(self, name:str) -> Body:
        for body in self._bodies:
            if body.name == name:
                return body
        
        raise KeyError(f"No body named {name!r}")
        
    def add_force(self, generator: ForceGenerator) -> ForceGenerator:
        for existing in self._generators:
            if generator.label == existing.label:
                raise ValueError("Generator exists already")
        self._generators.append(generator)
        return generator

    def find_force(self, label:str) -> ForceGenerator | None:
        for generator in self._generators:
            if generator.label == label:
                return generator
        return None

    def step(self, dt:float) -> None:
        if dt <= 0:
            raise ValueError("dt must be positive")

        for body in self._bodies:
            body.clear_forces()
        
        for generator in self._generators:
            if generator.enabled:
                generator.apply(self)

        for body in self._bodies:
            self.integrator.step(body, dt)

        self.time += dt

    
    def mechanical_energy(self, body:Body) -> float:
        kinetic =  body.kinetic_energy()
        potential = 0.0
        
        for generator in self._generators:
            if not generator.enabled:
                continue
            potential += generator.potential_energy(body)

        return kinetic + potential


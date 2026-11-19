from __future__ import annotations
from collections import deque
from dataclasses import dataclass

from physlab.core.vector2d import Vector2D
from physlab.physics.world import World

@dataclass(frozen=True)
class Sample:
    time: float
    position: Vector2D
    velocity: Vector2D
    acceleration: Vector2D


class Recorder:
    def __init__(self, max_samples: int = 600) -> None:

        if max_samples < 1:
            raise ValueError("There must be at least one sample.")
        
        self.max_samples = max_samples

        self.samples_per_body: dict[str, deque[Sample]] = {}

    def sample(self, world: World) -> None:

        for body in world.bodies:

            if body.name not in self.samples_per_body:
                self.samples_per_body[body.name] = deque(maxlen=self.max_samples)

            self.samples_per_body[body.name].append(Sample(time= world.time, position= body.position, velocity= body.velocity, acceleration= body.acceleration))
            

    def samples(self, body_name: str) -> tuple[Sample, ...]:

        if body_name in self.samples_per_body:
            return tuple(self.samples_per_body[body_name])
        
        return ()

    def positions(self, body_name: str) -> list[Vector2D]:

        body_positions = []
        
        for sample in self.samples(body_name):
            body_positions.append(sample.position)
        
        return body_positions
        
  
    def clear(self)-> None:
        self.samples_per_body.clear()


            



        
            



from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from physlab.physics.world import World


@dataclass(frozen=True)
class Parameter():
    key:str # v0
    label:str # launch speed
    unit:str # m/s, °, 
    minimum:float
    maximum:float
    default:float
    step:float
    kind: str = "slider" # slider or toggle(1, 0)

    def __post_init__(self) -> None:
        if self.minimum > self.default or self.default > self.maximum:
            raise ValueError("Default must be between min and max")
        elif self.step <= 0:
            raise ValueError("step must be greater than 0")
        elif self.kind != "slider" and self.kind != "toggle":
            raise ValueError("kind accepts only 'slider' or 'toggle'")
        
    def clamp(self, value:float)->float:
        if value < self.minimum:
            return self.minimum
        elif value > self.maximum:
            return self.maximum
        else:
            return value
        

# REVIEW 4 (Claude, 2026-10-09). Two small fixes left; with them every Vector2D and Body test passes (checked in a copy).
from __future__ import annotations
from physlab.core.constants import FLOAT_TOLERANCE
from dataclasses import dataclass
import math



@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __post_init__(self):
        for name, value in (("x", self.x), ("y", self.y)):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be int or float, got {type(value).__name__}")


#-------- Class Methods --------------------------
    @classmethod
    def zero(cls) -> Vector2D:
        return cls(0.0, 0.0)
    
    @classmethod
    def from_polar(cls, magnitude: float, angle: float) -> Vector2D:
        return cls(magnitude * math.cos(angle), magnitude * math.sin(angle))

    


# ----- OPERATOR OVERLOADING (Instance methods) ----------------

    def __add__(self, other: Vector2D) -> Vector2D:
        if not isinstance(other, Vector2D):
            return NotImplemented 
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        if not isinstance(other, Vector2D):
            return NotImplemented 
        return Vector2D(self.x - other.x, self.y - other.y)    

    def __mul__(self, scalar: float) -> Vector2D:
        if not isinstance(scalar, (int, float)):
            return NotImplemented 
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector2D:
        
        if not isinstance(scalar, (int, float)):
            return NotImplemented 
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector2D:

        if not isinstance(scalar, (int, float)):
            return NotImplemented 

        return Vector2D(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Vector2D:
        return Vector2D(self.x * -1, self.y * -1)

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f})"

# ---------- Methods --------------------------------------------------

    def magnitude(self) -> float:
        return math.hypot(self.x, self.y)

    def magnitude_squared(self) -> float:
        return self.x*self.x + self.y*self.y

    def is_zero(self, tol: float = FLOAT_TOLERANCE) -> bool:
        return self.magnitude() <= tol

    
    def normalized(self) -> Vector2D:
        if self.is_zero():
            raise ValueError("Cant divide a zero-vector")
        
        return self / self.magnitude()

    def dot(self, other: Vector2D) -> float:
        return (self.x * other.x) + (self.y * other.y)

    def cross(self, other: Vector2D) -> float:
        return (self.x * other.y) - (self.y * other.x)

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

     

    

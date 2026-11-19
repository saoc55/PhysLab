from __future__ import annotations
from typing import Final

STANDARD_GRAVITY: Final[float] = 9.81 #m/s^2
AIR_DENSITY: Final[float] = 1.225 #kg/m^3
SPHERE_DRAG_COEFFICIENT: Final[float] = 0.47 
PHYSICS_DT: Final[float] = 1 / 240 #s
MAX_STEPS_PER_ADVANCE: Final[int] = 240 #steps
FLOAT_TOLERANCE: Final[float] = 1e-12 


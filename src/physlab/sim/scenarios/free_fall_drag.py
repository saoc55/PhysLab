from __future__ import annotations
import math
from physlab.core.constants import AIR_DENSITY, STANDARD_GRAVITY
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body
from physlab.physics.forces import QuadraticDrag, UniformGravity
from physlab.physics.world import World
from physlab.sim.scenario import Scenario
from physlab.sim.parameters import Parameter

class FreeFallDragScenario(Scenario):

    name = "Free fall with drag"
    description= "A ball dropped from rest speeds up until air drag balances its weight; from then on it falls at the terminal velocity."
    
    def parameters(self) -> list[Parameter]:
        parameters = [Parameter(key="mass", label="Mass", unit="kg", minimum=0.1, maximum=10, default=1, step=0.1, kind="slider"),
                      Parameter(key="area", label="Cross section", unit="m²", minimum=0.001, maximum=0.1, default=0.01, step=0.001, kind="slider"),
                      Parameter(key="cd", label="Drag coefficient", unit="", minimum=0.1, maximum=2, default=0.47, step=0.01, kind="slider"),
                      Parameter(key="height", label="Drop height", unit="m", minimum=100, maximum=5000, default=3000, step=50, kind="slider")]

        return parameters

    def build(self, values: dict[str, float]) -> World:
        world = World()

        body = Body(name="ball", mass= values["mass"], position=Vector2D(0, values["height"]))
        world.add_body(body)
        world.add_force(UniformGravity())
        world.add_force(QuadraticDrag(area = values["area"], cd=values["cd"]))

        self._last_values = values
        return world

    def is_finished(self, world: World) -> bool:
        ball = world.get_body("ball")
        return ball.position.y <= 0
         
    def view_bounds(self, values: dict[str, float])->tuple[float, float, float, float]:
        h = values["height"]
        return (-0.1 * h, -0.05 * h, 0.1 * h, 1.05 * h)

    def readouts(self, world: World) -> list[tuple[str, str]]:
        ball = world.get_body("ball")
        values = self._last_values

        v_t = math.sqrt((2 * ball.mass * STANDARD_GRAVITY) / (AIR_DENSITY * values["cd"] * values["area"]))

        speed = ball.velocity.magnitude()
            
        return [("terminal velocity", f"{v_t:.3f} m/s"),
                    ("speed / v_t", f"{100 * (speed / v_t):.3f} %")]


        
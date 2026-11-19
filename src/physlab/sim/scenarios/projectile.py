from __future__ import annotations

import math
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body
from physlab.sim.scenario import Scenario
from physlab.sim.parameters import Parameter
from physlab.physics.forces import UniformGravity, QuadraticDrag
from physlab.physics.world import World

class ProjectileScenario(Scenario):

    name = "Projectile"
    description = "A ball launched at a chosen speed and angle. Without air it follows a parabola; with drag the path is shorter and steeper on the way down."

    def parameters(self)-> list[Parameter]:
        parameters = [Parameter(key= "v0", label="Launch speed", unit="m/s", minimum=0, maximum=50, default=20, step=0.5, kind="slider"),
                      Parameter(key= "angle", label="Launch angle", unit="°", minimum=0, maximum=90, default=45, step=1, kind="slider" ),
                      Parameter(key="h0", label="Launch height", unit="m", minimum=0, maximum=50, default=0, step=0.5, kind="slider"),
                      Parameter(key="g", label="Gravity", unit="m/s²", minimum=0, maximum=25, default=9.81, step=0.01, kind="slider"),
                      Parameter(key="mass", label="Mass", unit="kg", minimum=0.1, maximum=10, default=1, step=0.1, kind="slider"),
                      Parameter(key="drag", label="Air drag", unit="", minimum=0, maximum=1, default=0, step=1, kind="toggle")]
        return parameters
   

    def build(self, values:dict[str, float]) -> World:
        world = World()

        ball = Body(name="ball", mass = values["mass"], radius=0.11, position=Vector2D(0,values["h0"]), velocity=Vector2D.from_polar(values["v0"], math.radians(values["angle"])))
        world.add_body(ball)
        world.add_force(UniformGravity(values["g"]))

        if values["drag"] == 1:
            world.add_force(QuadraticDrag(area=math.pi * 0.11**2))
        
        self._last_values = values
        return world

    def is_finished(self, world:World) -> bool:
        ball = world.get_body("ball")
        return world.time > 0  and ball.position.y <= 0 and ball.velocity.y < 0
       
    def _range_and_apex(self, values: dict[str, float]) -> tuple[float, float]:
        rads = math.radians(values["angle"])
        vx, vy = math.cos(rads)*values["v0"], math.sin(rads)*values["v0"]
        apex = values["h0"] + vy**2/(2*values["g"])
        t = (vy + math.sqrt(vy**2 + 2*values["g"]*values["h0"])) / values["g"]
        r = vx*t
        return (r, apex)

 
    def view_bounds(self, values: dict[str, float]) -> tuple[float, float, float, float]:
        if values["g"] == 0:
            return (-1,-1,20,12)
    
        r, apex = self._range_and_apex(values)

        right = 1.1 * r
        top = 1.1 * apex

        if right < 5:
            right = 5
        if top < 3:
            top = 3
        
        return (-1, -1, right, top) 
        
    def readouts(self, world: World) -> list[tuple[str, str]]:
        values = self._last_values 

        if values["g"] == 0:
            return [("analytic range", "none (g = 0)"),
                    ("analytic apex", "none (g = 0)")]
        
        r, apex = self._range_and_apex(self._last_values)
        return [("analytic range", f"{r:.3f} m"),
                ("analytic apex", f"{apex:.3f} m")]
        
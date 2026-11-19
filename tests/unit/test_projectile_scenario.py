import pytest
from physlab.core.vector2d import Vector2D
from physlab.sim.parameters import Parameter
from physlab.sim.scenarios.projectile import ProjectileScenario



#-----------------------------------------------------------------AC4-------------------------------------------------------------

def test_parameter_list():

    keys = []
    params = ProjectileScenario().parameters()
    for parameter in params:
        keys.append(parameter.key)

    assert keys == ["v0", "angle", "h0", "g", "mass", "drag"]
    assert params ==  [Parameter(key= "v0", label="Launch speed", unit="m/s", minimum=0, maximum=50, default=20, step=0.5, kind="slider"),
                          Parameter(key= "angle", label="Launch angle", unit="°", minimum=0, maximum=90, default=45, step=1, kind="slider" ),
                          Parameter(key="h0", label="Launch height", unit="m", minimum=0, maximum=50, default=0, step=0.5, kind="slider"),
                          Parameter(key="g", label="Gravity", unit="m/s²", minimum=0, maximum=25, default=9.81, step=0.01, kind="slider"),
                          Parameter(key="mass", label="Mass", unit="kg", minimum=0.1, maximum=10, default=1, step=0.1, kind="slider"),
                          Parameter(key="drag", label="Air drag", unit="", minimum=0, maximum=1, default=0, step=1, kind="toggle")]


def test_default_parameter_values():
    parameters = ProjectileScenario().default_values()

    assert parameters == {"v0": 20, "angle": 45, "h0": 0, "g": 9.81, "mass": 1, "drag": 0}


#-----------------------------------------------------AC5--------------------------------------------------------------------

def test_new_world_per_build():
    scenario = ProjectileScenario()
    world1 = scenario.build(scenario.default_values())
    world2 = scenario.build(scenario.default_values())

    assert world1 is not world2
    assert world1.time == 0.0
    assert world2.time == 0.0 

    world2.step(dt=0.1)

    assert world1.time == 0.0
    assert world2.time == pytest.approx(0.1)


#--------------------------------------------------AC6------------------------------------------------------
def test_drag_settings():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())
    gen = []
    for force in world.generators:
        gen.append(force.label)
    assert tuple(gen) == ("weight",)

    
    values = scenario.default_values()
    values["drag"] = 1
    world2 = scenario.build(values)
    gens = []
    for force in world2.generators:
        gens.append(force.label)
    assert tuple(gens) == ("weight", "drag")


#--------------------------------------------------AC7------------------------------------------------------
def test_launch_state():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())
    

    ball = world.get_body("ball")    

    assert len(world.bodies) == 1
    assert ball.name == "ball"
    assert ball.mass == pytest.approx(1.0)
    assert ball.radius == 0.11
    assert ball.position.x == 0
    assert ball.position.y == 0
    assert ball.velocity.x == pytest.approx(14.142, abs=1e-3)
    assert ball.velocity.y == pytest.approx(14.142, abs=1e-3)


#--------------------------------------------------AC8------------------------------------------------------
def test_finish_rule():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())

    assert scenario.is_finished(world) == False
    
    world.step(dt = 1/240)
    ball = world.get_body("ball")

    max_steps = 2000
    steps = 0
    while ball.position.y > 0 and steps < max_steps:
        assert scenario.is_finished(world) == False
        world.step(dt = 1/240)
        steps += 1

    assert ball.position.y <= 0
    assert scenario.is_finished(world) == True



    
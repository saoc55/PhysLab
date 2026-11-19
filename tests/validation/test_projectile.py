import pytest

from physlab.sim.scenarios.projectile import ProjectileScenario
from physlab.physics.integrators import ExplicitEuler


#------------------------------------------------------------------AC9-----------------------------------------------------------------------------------
def test_projectile_accuracy():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())

    ball = world.get_body("ball")

    max_steps = 2000
    steps = 0
    apex = 0

    world.step(dt = 1/240)
    
    while ball.position.y > 0 and steps < max_steps:

        if ball.position.y > apex:
            apex = ball.position.y

        previous_y = ball.position.y
        previous_x = ball.position.x
        previous_time = world.time

        world.step(dt =1/240)
        steps += 1

    assert ball.position.y <= 0

    y1 = previous_y
    y2 = ball.position.y
    f = y1 / (y1 - y2)

    landing_x = previous_x + f * (ball.position.x - previous_x)
    flight_time = previous_time + f * (world.time - previous_time)

    assert apex == pytest.approx(10.19, rel=0.01)
    assert landing_x == pytest.approx(40.77, rel=0.01)
    assert flight_time == pytest.approx(2.883, rel=0.01)
   

#------------------------------------------------------------------AC10-----------------------------------------------------------------------------------
def test_energy_conservation():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())

    ball = world.get_body("ball")

    initial_energy = world.mechanical_energy(ball)
    assert initial_energy == pytest.approx(200, rel=0.01)

    max_steps = 2000
    steps = 0

    world.step(dt=1/240)

    while ball.position.y > 0 and steps < max_steps:
        world.step(dt=1/240)
        steps += 1

    landing_energy = world.mechanical_energy(ball)

    assert ball.position.y <= 0
    assert landing_energy == pytest.approx(initial_energy, rel=0.01)


#------------------------------------------------------------------AC11-----------------------------------------------------------------------------------
def test_integrator_comparison():
    scenario = ProjectileScenario()
    world = scenario.build(scenario.default_values())
    world.integrator = ExplicitEuler()
    ball = world.get_body("ball")

    initial_energy = world.mechanical_energy(ball)
    assert initial_energy == pytest.approx(200, rel=0.01)

    max_steps = 2000
    steps = 0

    world.step(dt=1/240)

    while ball.position.y > 0 and steps < max_steps:
        world.step(dt=1/240)
        steps += 1

    landing_energy = world.mechanical_energy(ball)

    assert ball.position.y <= 0
    assert landing_energy > initial_energy
    
#------------------------------------------------------------------AC12-----------------------------------------------------------------------------------
# REVIEW 3 (optional): helpers usually sit at the top, after the imports, so the tests below read top to bottom.
def _fly(world, dt = 1/240, max_steps = 2000):
    
    ball = world.get_body("ball")

    world.step(dt=dt)
    previous_x = ball.position.x
    previous_y = ball.position.y

    steps = 0

    while ball.position.y > 0 and steps < max_steps:
        previous_x = ball.position.x
        previous_y = ball.position.y

        world.step(dt=dt)
        steps += 1

    assert ball.position.y <= 0

    f = previous_y / (previous_y - ball.position.y)

    landing_x = previous_x + f * (ball.position.x - previous_x)

    return landing_x

    

def test_drag_effect():
    scenario = ProjectileScenario()
    world1 = scenario.build(scenario.default_values())

    range_no_drag = _fly(world1)

    values = scenario.default_values()
    values["drag"] = 1
    world2 = scenario.build(values)

    range_with_drag = _fly(world2)

    assert range_with_drag < range_no_drag


import math

import pytest

from physlab.core.constants import AIR_DENSITY, STANDARD_GRAVITY
from physlab.sim import scenarios 
from physlab.sim.scenarios.free_fall_drag import FreeFallDragScenario
from physlab.sim.scenarios.projectile import ProjectileScenario


def _terminal_velocity(values):
    vt = math.sqrt((2 * values["mass"] * STANDARD_GRAVITY) / (AIR_DENSITY * values["area"] * values["cd"]))
    return vt

def test_terminal_velocity_reference():
    scenario = FreeFallDragScenario()
    values = scenario.default_values()
    
    vt = _terminal_velocity(values)

    assert vt == pytest.approx(58.38, rel=0.001)

def test_speeding_up():
    scenario = FreeFallDragScenario()
    values = scenario.default_values()
    world = scenario.build(values)
    ball = world.get_body("ball")

    while world.time < 5.0:
        world.step(dt=1/240)

    speed = ball.velocity.magnitude()
    vt = _terminal_velocity(values)   

    expected_speed = vt * math.tanh((STANDARD_GRAVITY * world.time) / vt)
    assert speed == pytest.approx(expected_speed, rel=0.01)

def test_approach():
    scenario = FreeFallDragScenario()
    values = scenario.default_values()
    world = scenario.build(values)
    ball = world.get_body("ball")

    while world.time < 30.0:
        world.step(dt=1/240)

    speed = ball.velocity.magnitude()
    vt = _terminal_velocity(values) 

    assert speed == pytest.approx(vt, rel=0.01)

def test_no_overshoot():
    scenario = FreeFallDragScenario()
    values = scenario.default_values()
    world = scenario.build(values)  
    ball = world.get_body("ball")

    vt = _terminal_velocity(values)   

    while world.time < 30.0:
        world.step(dt=1/240)
        speed = ball.velocity.magnitude()
        assert speed <= 1.001 * vt

def test_registry():
    assert len(scenarios.SCENARIOS) == 2
    assert isinstance(scenarios.SCENARIOS[0], ProjectileScenario)
    assert isinstance(scenarios.SCENARIOS[1], FreeFallDragScenario)
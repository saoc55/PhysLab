import pytest
from physlab.sim.runner import SimulationRunner
from physlab.sim.scenarios.free_fall_drag import FreeFallDragScenario
from physlab.sim.scenarios.projectile import ProjectileScenario

@pytest.fixture
def scenario():
    scenario = FreeFallDragScenario()
    return scenario

def test_initial_state(scenario):
    
    runner = SimulationRunner(scenario)
    values = scenario.default_values()

    assert runner.paused is True
    assert runner.finished is False
    assert runner.world.time == 0.0
    assert runner.values == values   
    
    for body in runner.world.bodies:
        assert len(runner.recorder.samples(body.name)) == 1
        assert runner.recorder.samples(body.name)[0].time == 0.0
        
def test_paused_state(scenario):

    runner = SimulationRunner(scenario)
    assert runner.advance(1.0) == 0
    assert runner.world.time == 0
    
    runner.resume()
    assert runner.advance(0.0) == 0

def test_fixed_steps(scenario):

    runner = SimulationRunner(scenario)
    runner.resume()
    
    assert runner.advance(0.1) == 24
    assert runner.world.time == pytest.approx(0.1)

def test_carry_over(scenario):

    runner = SimulationRunner(scenario)
    runner.resume()
    assert runner.advance(1/480) == 0

    assert runner.advance(1/480) == 1

def test_backlog_guard(scenario):

    runner = SimulationRunner(scenario)
    runner.resume()
    assert runner.advance(10.0) == 240
    assert runner.world.time == pytest.approx(1.0)

    assert runner.advance(0.0) == 0

def test_single_step(scenario):

    runner = SimulationRunner(scenario)
    runner.step_once()
    assert runner.world.time == pytest.approx(1/240)
    assert runner.paused is True

    runner.resume()
    runner.step_once()
    assert runner.world.time == pytest.approx(2/240)
    assert runner.paused is False

def test_parameter_change():

    runner = SimulationRunner(ProjectileScenario())
    runner.step_once()
    runner.set_value("v0", 999)

    assert runner.values["v0"] == 50
    assert runner.world.time == 0.0
    
    assert runner.paused is True

    values = runner.values.copy()
    with pytest.raises(KeyError):
        runner.set_value("speed", 1)

    assert runner.values == values

def test_finish(scenario):

    runner = SimulationRunner(scenario)
    runner.resume()

    max_calls = 500
    for _ in range(max_calls):
        if runner.finished:
            break
        else:
            runner.advance(3)

    assert runner.finished is True
    assert runner.paused is True

    assert runner.advance(1) == 0

    w_time = runner.world.time

    runner.step_once()
    assert runner.world.time == w_time

    runner.resume()
    assert runner.paused is True

    assert runner.recorder.samples("ball")[-1].time == runner.world.time

def test_reset_callback(scenario):

    runner = SimulationRunner(scenario)
    counter = {"calls": 0}

    #simulated function
    def on_reset_hook():
        counter["calls"] += 1
    
    # Attach the hook (no parentheses)
    runner.on_reset = on_reset_hook

    #1st reset call via set_value
    runner.set_value("mass", 2)
    assert counter["calls"] == 1

    #2nd reset call via load_scenario
    runner.load_scenario(scenario)
    assert counter["calls"] == 2

def test_sampling_rate(scenario):

    runner = SimulationRunner(scenario, sample_every = 4)

    assert len(runner.recorder.samples("ball")) == 1

    for _ in range(8):
        runner.step_once()

    assert len(runner.recorder.samples("ball")) == 3
    

    


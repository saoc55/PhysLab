import pytest
from dataclasses import FrozenInstanceError
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body
from physlab.physics.world import World
from physlab.sim.recorder import Recorder


@pytest.fixture
def world():
    world = World()
    world.add_body(Body(name="a", mass=1, position=Vector2D(0,0), velocity=Vector2D(1,1)))
    world.add_body(Body(name="b", mass=1, position=Vector2D(0,0), velocity=Vector2D(1,1)))
    return world

def test_sampling(world):

    recorder = Recorder()
    for _ in range(3):
        
        recorder.sample(world)

        samples_a = recorder.samples("a")
        samples_b = recorder.samples("b")
        body_a = world.get_body("a")
        body_b = world.get_body("b")

        assert samples_a[-1].position == body_a.position
        assert samples_b[-1].position == body_b.position

        assert samples_a[-1].velocity == body_a.velocity
        assert samples_b[-1].velocity == body_b.velocity

        assert samples_a[-1].acceleration == body_a.acceleration
        assert samples_b[-1].acceleration == body_b.acceleration
        
        world.step(dt=0.1)

    times_a = []
    for sample in samples_a:
        times_a.append(sample.time)

    times_b = []
    for sample in samples_b:
        times_b.append(sample.time)


    assert times_a == pytest.approx([0.0, 0.1, 0.2])
    assert times_b == pytest.approx([0.0, 0.1, 0.2])

# REVIEW 9 (optional): the "collect the times of a body" loop now appears four times. One helper at the top would cut it.
def test_bounded_history(world):
    recorder = Recorder(max_samples=5)
    for _ in range(8):
        recorder.sample(world)
        world.step(dt=0.1)

    samples_a = recorder.samples("a")
    samples_b = recorder.samples("b")

   
    assert len(samples_a) == 5
    assert len(samples_b) == 5

    times_a = []
    for sample in samples_a:
        times_a.append(sample.time)

    times_b = []
    for sample in samples_b:
        times_b.append(sample.time)

    assert times_a == pytest.approx([0.3, 0.4, 0.5, 0.6, 0.7])
    assert times_b == pytest.approx([0.3, 0.4, 0.5, 0.6, 0.7])
    
def test_unknown_names(world):
    recorder = Recorder()
    recorder.sample(world)
    samples_c = recorder.samples("c")

    assert samples_c == ()

    recorder.clear()
    assert recorder.samples("a") == ()
    assert recorder.samples("b") == ()

    with pytest.raises(ValueError):
        Recorder(max_samples = 0)

    with pytest.raises(ValueError):
        Recorder(max_samples = -1)

def test_frozen_snapshots(world):
    recorder = Recorder()
    recorder.sample(world)
    position_a = world.get_body("a").position

    world.step(dt=0.1)

    samples_a = recorder.samples("a")

    assert samples_a[0].position == position_a
    assert samples_a[0].position != world.get_body("a").position

    with pytest.raises(FrozenInstanceError):
        samples_a[0].position = Vector2D(0,0)

def test_positions(world):

    recorder= Recorder()

    for _ in range(5):
        recorder.sample(world)
        world.step(dt=0.1)

    samples_a = recorder.samples("a")

    sample_pos = []
    for sample in samples_a:
        sample_pos.append(sample.position)

    positions_a = recorder.positions("a")

    assert positions_a == sample_pos

    positions_c = recorder.positions("c")

    assert positions_c == []

    
    

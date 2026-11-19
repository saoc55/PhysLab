
import pytest
from physlab.physics.world import World
from physlab.physics.integrators import SemiImplicitEuler, ExplicitEuler
from physlab.physics.body import Body
from physlab.core.vector2d import Vector2D
from physlab.physics.forces import UniformGravity, QuadraticDrag


#---------------------------------------------AC1---------------------------------------------
def test_initial_state_default():
    world = World()

    assert world.time == 0.0
    assert isinstance(world.integrator, SemiImplicitEuler)
    assert not world.bodies #empty tuple.
    assert not world.generators #empty tuple.

def test_initial_state_given():
    integrator = ExplicitEuler()
    world = World(integrator= integrator)

    assert world.integrator is integrator


#---------------------------------------------Fixture: world with 3 bodies (AC2 to AC6)---------------------------------------------
@pytest.fixture
def world():
    world = World()
    
    world.add_body(Body(name = "ball1", mass = 1.0, position = Vector2D(0,0)))  
    world.add_body(Body(name = "ball2", mass = 2.0, position = Vector2D(0,0)))
    world.add_body(Body(name = "ball3", mass = 1.5, position = Vector2D(0,0)))

    return world


#---------------------------------------------AC2---------------------------------------------
def test_add_body_returns_body(world):
    body = Body(name="ball", mass=1.0, position=Vector2D(0,0))

    result = world.add_body(body)
    assert result is body

    names = tuple(body.name for body in world.bodies)
    assert names == ("ball1", "ball2", "ball3", "ball")


#---------------------------------------------AC3---------------------------------------------
def test_unique_body_names(world):
    original = world.get_body("ball1")

    with pytest.raises(ValueError):
        world.add_body(Body(name="ball1", mass=2.0, position=Vector2D(2,0)))

    assert world.get_body("ball1") is original
    assert len(world.bodies) == 3    


#---------------------------------------------AC4---------------------------------------------
def test_unique_generator_names(world):
    world.add_force(UniformGravity())

    with pytest.raises(ValueError):
        world.add_force(UniformGravity(5.0))

    assert len(world.generators) == 1


def test_unique_generator_names_pos(world):
    world.add_force(UniformGravity())
    
    world.add_force(QuadraticDrag(0.01))

    labels = tuple(generator.label for generator in world.generators)

    assert labels == ("weight", "drag")
    
    

#---------------------------------------------AC5---------------------------------------------
def test_get_body_in_empty_world():
    world = World()

    with pytest.raises(KeyError):
        world.get_body("ball")

def test_get_unknown_raises_error(world):
    with pytest.raises(KeyError):
        world.get_body("ball4")


def test_get_body_pos(world):
    body4 = Body(name = "ball4", mass = 1.0, position = Vector2D(0,0))
    world.add_body(body4)
    assert world.get_body("ball4") is body4


#---------------------------------------------AC6---------------------------------------------
def test_find_force(world):
    gravity, drag = UniformGravity(), QuadraticDrag(0.01)

    world.add_force(gravity)
    world.add_force(drag)

    assert world.find_force("force") is None
    assert world.find_force("weight") is gravity


#---------------------------------------------Fixture: 1 kg ball with gravity (AC7 to AC12)---------------------------------------------
@pytest.fixture
def world_with_gravity():
    body = Body(name="ball", mass=1.0, position=Vector2D(0,0))
    gravity = UniformGravity()
    world = World()
    world.add_body(body)
    world.add_force(gravity)

    return world


#---------------------------------------------AC7---------------------------------------------
def test_fresh_forces_each_step(world_with_gravity):
    world_with_gravity.step(dt= 0.1)
    world_with_gravity.step(dt= 0.1)
    ball = world_with_gravity.get_body("ball")
    assert len(ball.forces) == 1
    
    assert ball.forces[0].label == "weight"


#---------------------------------------------AC8---------------------------------------------
def test_disabled_generators(world_with_gravity):
    gravity = world_with_gravity.find_force("weight")
    gravity.enabled = False
    ball = world_with_gravity.get_body("ball")
    ball.position = Vector2D(0,10)
    world_with_gravity.step(dt=0.1)
    
    assert ball.position.x == 0.0
    assert ball.position.y == 10.0
    assert ball.velocity.x == 0.0
    assert ball.velocity.y == 0.0

    assert not ball.forces


#---------------------------------------------AC9---------------------------------------------
@pytest.mark.parametrize("integrator, p_x, p_y, v_x, v_y",[
   (SemiImplicitEuler(), 0, -0.1, 0, -1), (ExplicitEuler(), 0, 0, 0, -1)
])
def test_step_order_and_integrator(world_with_gravity, integrator, p_x, p_y, v_x, v_y):
    gravity = world_with_gravity.find_force("weight")
    gravity.g = 10
    
    world_with_gravity.integrator = integrator
    world_with_gravity.step(dt=0.1)
    ball = world_with_gravity.get_body("ball")

    assert ball.position.x == pytest.approx(p_x)
    assert ball.position.y == pytest.approx(p_y)
    assert ball.velocity.x == pytest.approx(v_x)
    assert ball.velocity.y == pytest.approx(v_y)
    


#---------------------------------------------AC10--------------------------------------------
def test_time(world_with_gravity):
    for _ in range(240):
        world_with_gravity.step(dt=1/240)

    assert world_with_gravity.time == pytest.approx(1.0)


def test_time_neg(world_with_gravity):
    with pytest.raises(ValueError):
        world_with_gravity.step(dt=0)
    with pytest.raises(ValueError):
        world_with_gravity.step(dt=-0.1)

    assert world_with_gravity.time == 0.0


#---------------------------------------------AC11--------------------------------------------
@pytest.mark.parametrize("enabled, position, velocity, expected", [
    (True, Vector2D(0,10), Vector2D(0,0), 98.1),
    (True, Vector2D(0,10), Vector2D(3,4), 110.6),
    (False, Vector2D(0,10), Vector2D(0,0), 0)
])
def test_mechanical_energy(world_with_gravity, enabled, position, velocity, expected):
    gravity = world_with_gravity.find_force("weight")
    gravity.enabled = enabled
    ball = world_with_gravity.get_body("ball")
    ball.position = position
    ball.velocity = velocity

    assert world_with_gravity.mechanical_energy(ball) == pytest.approx(expected)


#---------------------------------------------AC12--------------------------------------------
def test_read_only_collections(world_with_gravity):
    bodies = world_with_gravity.bodies
    world_with_gravity.add_body(Body(name="car", mass=2000, position=Vector2D(0,0)))

    assert len(bodies) == 1
    assert len(world_with_gravity.bodies) == 2

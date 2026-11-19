import pytest
from physlab.core.vector2d import Vector2D
from physlab.physics.integrators import Integrator, ExplicitEuler, SemiImplicitEuler
from physlab.physics.body import Body


@pytest.mark.parametrize("integrator_class", [ExplicitEuler, SemiImplicitEuler])
@pytest.mark.parametrize("mass, force, expected",[
    (2.0, Vector2D(4,0), Vector2D(2,0)),
    (1.0, Vector2D(0, -9.81), Vector2D(0, -9.81)),
    (4.0, Vector2D(-8, 2), Vector2D(-2, 0.5)),
    (5.0, Vector2D(0, 0), Vector2D(0,0))
])
def test_integrator_sets_acceleration(integrator_class, mass, force, expected):
    body = Body(name="ball", mass = mass, position=Vector2D(0,0))
    body.add_force("push", force)

    integrator_class().step(body, dt=0.1)

    assert body.acceleration.x == pytest.approx(expected.x)
    assert body.acceleration.y == pytest.approx(expected.y)

@pytest.mark.parametrize("integrator_class", [ExplicitEuler, SemiImplicitEuler])
@pytest.mark.parametrize("velocity, counter, dt, expected",[
    (Vector2D(1,0), 240, 1/240, Vector2D(1,0)),
    (Vector2D(2,-1), 60, 1/60, Vector2D(2,-1))
])
def test_uniform_motion(integrator_class, velocity, counter, dt, expected):
    body = Body(name = "ball", mass = 1.0, position= Vector2D(0,0), velocity= velocity)

    integrator = integrator_class()

    for _ in range(counter):
        integrator.step(body, dt=dt)

    assert body.position.x == pytest.approx(expected.x)
    assert body.position.y == pytest.approx(expected.y)
    assert body.velocity.x == pytest.approx(velocity.x)
    assert body.velocity.y == pytest.approx(velocity.y)


@pytest.mark.parametrize("velocity, ex_pos, ex_v", [
    (Vector2D(0, 0), Vector2D(0,0), Vector2D(0, -1)),
    (Vector2D(0, 2), Vector2D(0,0.2), Vector2D(0, 1))
])
def test_explicit_euler_order(velocity, ex_pos, ex_v):
    
    body = Body(name = "ball", mass = 1.0, position= Vector2D(0,0), velocity = velocity)
    body.add_force("push", Vector2D(0, -10))

    integrator = ExplicitEuler()
    integrator.step(body, dt=0.1)

    assert body.position.x == pytest.approx(ex_pos.x)
    assert body.position.y == pytest.approx(ex_pos.y)
    assert body.velocity.x == pytest.approx(ex_v.x)
    assert body.velocity.y == pytest.approx(ex_v.y)


@pytest.mark.parametrize("velocity, ex_pos, ex_v", [
    (Vector2D(0, 0), Vector2D(0,-0.1), Vector2D(0, -1)),
    (Vector2D(0, 2), Vector2D(0,0.1), Vector2D(0, 1))
])
def test_semi_implicit_euler_order(velocity, ex_pos, ex_v):
    
    body = Body(name = "ball", mass = 1.0, position= Vector2D(0,0), velocity = velocity)
    body.add_force("push", Vector2D(0, -10))

    integrator = SemiImplicitEuler()
    integrator.step(body, dt=0.1)

    assert body.position.x == pytest.approx(ex_pos.x)
    assert body.position.y == pytest.approx(ex_pos.y)
    assert body.velocity.x == pytest.approx(ex_v.x)
    assert body.velocity.y == pytest.approx(ex_v.y)


def test_integrator_cant_be_instantiated():
    with pytest.raises(TypeError, match="abstract"):
        Integrator()



@pytest.mark.parametrize("integrator_class", [ExplicitEuler, SemiImplicitEuler])
def test_display_names(integrator_class):
    integrator = integrator_class()

    assert len(integrator.name) > 0



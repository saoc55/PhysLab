import pytest
import dataclasses
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body, AppliedForce


@pytest.fixture
def body():
    return Body(name = "ball", mass = 2.0, position = Vector2D(0.00, 0.00))

@pytest.mark.parametrize("forces, expected_x, expected_y",[
    ([], 0 ,0 ),
    ([("push", Vector2D(3, 0))], 3, 0),
    ([("weight", Vector2D(0, -19.62)), ("push", Vector2D(4, 0))], 4, -19.62),
    ([("left", Vector2D(-5, 0)), ("right", Vector2D(5, 0))], 0, 0)
])
def test_net_force_returns_sum_of_forces(body, forces, expected_x, expected_y):
    for label, vector in forces:
        body.add_force(label, vector)

    result = body.net_force()

    assert result.x == pytest.approx(expected_x)
    assert result.y == pytest.approx(expected_y)


@pytest.mark.parametrize("forces",[
    ([]),
    ([("push", Vector2D(3, 0))]),
    ([("weight", Vector2D(0, -19.62)), ("push", Vector2D(4, 0))]),
    ([("left", Vector2D(-5, 0)), ("right", Vector2D(5, 0))])
])
def test_forces_returns_all_applied_forces(body, forces):

    for label, vector in forces:
        body.add_force(label, vector)

    stored = [(f.label, f.vector) for f in body.forces]

    assert stored == forces
    

def test_force_cant_be_edited(body):

    body.add_force("push", Vector2D(1,2))

    snapshot = body.forces
    body.add_force("weight", Vector2D(0, -19.62))

    assert isinstance(snapshot, tuple)
    assert len(snapshot) == 1 # the earlier copy did not grow
    assert len(body.forces) == 2 # the body itself did


@pytest.mark.parametrize("forces",[
    ([("push", Vector2D(3, 0))]),
    ([("weight", Vector2D(0, -19.62)), ("push", Vector2D(4, 0))]),
    ([("left", Vector2D(-5, 0)), ("right", Vector2D(5, 0))])
])
def test_clearing(body, forces):

    for label, vector in forces:
        body.add_force(label, vector)

    snapshot = body.forces
    body.clear_forces()

    assert len(snapshot) > 0
    assert len(body.forces) == 0

@pytest.mark.parametrize("name, mass, radius",[
    ('', 2, 0.1),
    ('ball', 0, 0.1),
    ('ball', -1, 0.1),
    ('ball', 2, 0)
])
def test_body_attribute_validation(name, mass, radius):
    with pytest.raises(ValueError):
        body = Body(name= name, mass= mass, position=Vector2D(0, 0), radius= radius)
        


@pytest.mark.parametrize("mass, velocity, expected", [
    (2.0, Vector2D(0, 0),    0.0),    # at rest: no kinetic energy
    (2.0, Vector2D(3, 4),   25.0),    # spec example: |v| = 5, ½·2·25
    (2.0, Vector2D(-3, -4), 25.0),    # direction does not matter, only speed
    (1.0, Vector2D(10, 0),  50.0),    # ½·1·100
    (4.0, Vector2D(0, -5),  50.0),    # moving straight down: ½·4·25
    (0.5, Vector2D(2, 0),    1.0),    # light body: ½·0.5·4
])
def test_kinetic_energy_calculation(mass, velocity, expected):

    body = Body(name = "ball", mass = mass, position = Vector2D(0,0), velocity = velocity)

    assert body.kinetic_energy() == pytest.approx(expected)


def test_default_values(body):

    assert body.velocity == Vector2D(0,0)
    assert body.acceleration == Vector2D(0,0)
    assert body.radius == 0.1
    assert body.forces == ()


def test_appliedforces_are_immutable():

    force = AppliedForce("weight", Vector2D(0, -9.81))

    with pytest.raises(dataclasses.FrozenInstanceError):
        force.label = "gravitational pull"

    with pytest.raises(dataclasses.FrozenInstanceError):
        force.vector = Vector2D(0, -10)
    


    




 

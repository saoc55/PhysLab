# REVIEW 3 (Claude, 2026-10-12). One blocker (AC7 table), two wrong expectations (label, validation rows). forces.py fixes are still open too.
# REVIEW: Still to write: AC9 apply() with a stand in world, AC10 drag potential energy is 0.0 (see chat).
import pytest
import dataclasses
from physlab.core.vector2d import Vector2D
from physlab.physics.body import Body
from physlab.physics.forces import ForceGenerator, BodyForce, UniformGravity, QuadraticDrag



def test_abstract_force_classes_cannot_be_instantiated():
    with pytest.raises(TypeError):
        ForceGenerator("x")
    with pytest.raises(TypeError):
        BodyForce("y")



# ---------------- Gravity ---------------------------------

@pytest.mark.parametrize("mass, g, expected", [
    (2.0, 9.81,  -19.62),   # spec example
    (1.0, 9.81,   -9.81),   # 1 kg: force equals g in size
    (0.5, 9.81,   -4.905),  # light body
    (2.0, 1.62,   -3.24),   # Moon gravity: same mass, smaller force
    (5.0, 0.0,     0.0),    # g = 0: no weight at all
])
def test_uniformgravity_applies_downward_force(mass, g, expected):
    body = Body(name = "mass1", mass= mass, position = Vector2D(0,0))
    force = UniformGravity(g).force_on(body)

    assert force.x == pytest.approx(0.0)
    assert force.y == pytest.approx(expected)

def test_gravity_validation():
    with pytest.raises(ValueError):
        UniformGravity(g = -1)

def test_gravity_label():
    
    force = UniformGravity()
    assert force.label == "weight"


@pytest.mark.parametrize("mass, position, expected", [
    (2.0, Vector2D(0, 10), 196.2),
    (5.0, Vector2D(3, 10), 490.5),
    (2.0, Vector2D(0, 2.5), 49.05),
    (2.0, Vector2D(0, 0), 0.0),
    (2.0, Vector2D(0, -5), -98.1)
])
def test_gravity_potential_energy(mass, position, expected):
    body = Body(name = "ball", mass = mass, position= position)

    gravity  = UniformGravity()

    assert gravity.potential_energy(body) == pytest.approx(expected)

#-------------------- DRAG ----------------------------------

def test_drag_at_rest():

    body = Body(name="ball", mass=2, position=Vector2D(0,0))
    force = QuadraticDrag(area = 1.0).force_on(body)

    assert force.x == pytest.approx(0.0)
    assert force.y == pytest.approx(0.0)

@pytest.mark.parametrize("velocity, rho, cd, area, expected",[
    (Vector2D(3,4), 1, 1 , 2, Vector2D(-15, -20)),
    (Vector2D(-3,-4), 1, 1 , 2, Vector2D(15, 20))
])
def test_drag_size(velocity, rho, cd, area, expected):
    body = Body(name="ball", mass=1, position=Vector2D(0,0), velocity=velocity)

    drag = QuadraticDrag(area = area, rho = rho, cd = cd).force_on(body)

    assert drag.x == pytest.approx(expected.x)
    assert drag.y == pytest.approx(expected.y)



@pytest.mark.parametrize("velocity",[
    Vector2D(1, 0),
    Vector2D(0, -3),
    Vector2D(-2, 5),
    Vector2D(3, 4)
])
def test_drag_direction_opposite_to_velocity(velocity, area, expected):
    body = Body(name = "ball", mass = 1.0, position= Vector2D(0,0), velocity=velocity)
    drag = QuadraticDrag(area=1).force_on(body)

    assert drag.dot(velocity) < 0
    assert drag.cross(velocity) == pytest.approx(0.0, abd=1e-9)


@pytest.mark.parametrize("area, rho, cd", [
    (-1, 1, 1),
    (3, -1, 1),
    (4, 1, 0.5),
    (0, 1 ,1),
])
def test_drag_parameter_validation(area, rho, cd):
    with pytest.raises(ValueError):
        QuadraticDrag(area, rho, cd)


from types import SimpleNamespace

class ConstantForce(BodyForce):
    def force_on(self, Body):
        return Vector2D(1,0)
    
def test_apply_adds_force_to_every_body():
    bodies = [Body(name=n, mass=1.0, position=Vector2D(0,0)) for n in ("a", "b", "c")]
    world = SimpleNamespace(bodies=bodies)

    ConstantForce("test").apply(world)

    for body in bodies:
        assert len(body.forces) == 1
        assert body.forces[0].label == "test"
        assert body.forces[0].vector == Vector2D(1,0)


@pytest.mark.parametrize("position, velocity", [
    (Vector2D(0,0), Vector2D(0,0)),
    (Vector2D(0,10), Vector2D(3,4)),
    (Vector2D(5,-2), Vector2D(-1,0))
])
def test_drag_has_no_potential_energy(position, velocity):
    body = BodyForce(name="ball", mass=2.0, position=position, velocity=velocity)
    assert QuadraticDrag(area=1.0).potential_energy(body) == 0.0
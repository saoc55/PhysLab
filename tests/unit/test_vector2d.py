# REVIEW 4 (Claude, 2026-10-09). All 14 ACs now have tests. Three small fixes below.
import pytest
import math
import operator
import dataclasses
from physlab.core.vector2d import Vector2D
from physlab.core.constants import FLOAT_TOLERANCE

@pytest.mark.parametrize("x, y",[
    (1,2),
    (1.5, -2.25),
    (3, 0.5),
    (0,0)
])
def test_construction_accepts_real_nums(x,y):
    vector = Vector2D(x,y)
    assert vector.x == x
    assert vector.y == y

@pytest.mark.parametrize("x,y", [
    ("1",2),
    (1,"2"),
    (None, 0),
    (True, 0),
    (0, False),
    ([1],2)
])
def test_construction_rejects_non_numbers(x,y):
    with pytest.raises(TypeError):
        Vector2D(x,y)


def test_immutability():
    vector = Vector2D(1, 2)

    with pytest.raises(dataclasses.FrozenInstanceError):
        vector.x = 3

    with pytest.raises(dataclasses.FrozenInstanceError):
        vector.y = 4



@pytest.mark.parametrize("a, b, expected",[
    (Vector2D(1,2), Vector2D(3,4), Vector2D(4,6)),
     (Vector2D(-1,2), Vector2D(1,-2), Vector2D(0,0)),
     (Vector2D(0.1,0), Vector2D(0.2,0), Vector2D(0.3,0))
    ])
def test_addition_sums_components(a, b , expected):
    result = a + b
    assert result.x == pytest.approx(expected.x)
    assert result.y == pytest.approx(expected.y)

@pytest.mark.parametrize("op, v1, v2", [
    (operator.add, Vector2D(1,2), 5),
    (operator.add, 5, Vector2D(1,2)),
    (operator.sub, Vector2D(3,4), "b"),
    (operator.mul, Vector2D(1,2), "b"),
    (operator.mul, Vector2D(1,2), Vector2D(4,5)),
    (operator.truediv, Vector2D(1,2), "a"),
    (operator.truediv, Vector2D(1,2), Vector2D(4,5))
])
def test_reject_unsupported_operands(op, v1, v2):
    with pytest.raises(TypeError):
        op(v1, v2)




@pytest.mark.parametrize("a, b, expected",[
    (Vector2D(1,2), Vector2D(3,4), Vector2D(-2,-2)),
     (Vector2D(-1,2), Vector2D(1,-2), Vector2D(-2,4)),
     (Vector2D(0.1,0), Vector2D(0.2,0), Vector2D(-0.1,0))
    ])
def test_subtraction_subtracts_components(a, b, expected):
    result = a - b
    assert result.x == pytest.approx(expected.x)
    assert result.y == pytest.approx(expected.y)


@pytest.mark.parametrize("a, expected",[
    (Vector2D(1,2), Vector2D(-1,-2)),
     (Vector2D(-1,2), Vector2D(1,-2)),
     (Vector2D(0.1,0), Vector2D(-0.1,0))
    ])
def test_negation(a, expected):
    result = -a
    assert result.x == expected.x
    assert result.y == expected.y


@pytest.mark.parametrize("a, scalar, expected",[
    (Vector2D(1,2), 2, Vector2D(2,4)),
     (Vector2D(-1,2), 3, Vector2D(-3,6)),
     (Vector2D(0.1,0), 10, Vector2D(1,0))
    ])
def test_scalar_multiplication_and_rmul(a, scalar, expected):
    result = a * scalar
    result2 = scalar * a
    assert result.x == pytest.approx(expected.x)
    assert result.y == pytest.approx(expected.y)
    assert result2.x == pytest.approx(expected.x)
    assert result2.y == pytest.approx(expected.y)



def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError): # [x,y] / 0
        (Vector2D(1,2) / 0)


@pytest.mark.parametrize("a, scalar, expected",[
    (Vector2D(1,2), 2, Vector2D(0.5,1)),
    (Vector2D(3,6), 3, Vector2D(1, 2)),
    (Vector2D(100,0), 10, Vector2D(10,0))
    ])
def test_scalar_division(a, scalar, expected):
    result = a / scalar
    assert result.x == pytest.approx(expected.x)
    assert result.y == pytest.approx(expected.y)


@pytest.mark.parametrize("a, expected",[
    (Vector2D(4,3), 5),
    (Vector2D(5,12), 13),
    (Vector2D(6,8), 10)
    ])
def test_magnitude_returns_length(a, expected):
    assert a.magnitude() == pytest.approx(expected)


@pytest.mark.parametrize("a, expected",[
    (Vector2D(4,3), 25),
     (Vector2D(2,1), 5),
     (Vector2D(3,3), 18)
    ])
def test_magnitude_squared_returns(a, expected):
    assert a.magnitude_squared() == pytest.approx(expected)


@pytest.mark.parametrize("a, expected",[
    (Vector2D(0,0), True),
     (Vector2D(1e-13, 0), True),
     (Vector2D(1e-6, 0), False)
    ])
def test_is_zero_returns_True_under_tolerance(a, expected):
    assert a.is_zero() == expected


@pytest.mark.parametrize("a, expected",[
    (Vector2D(4,3), Vector2D(0.8, 0.6)),
     (Vector2D(0,5), Vector2D(0, 1)),
     (Vector2D(-3,4), Vector2D(-0.6, 0.8))
    ])
def test_normalize_returns_vector_length_1(a, expected): 
    result = a.normalized()   
    assert result.x == pytest.approx(expected.x)
    assert result.y == pytest.approx(expected.y)
    assert result.magnitude() == pytest.approx(1)

def test_normalize_zero_vector():
    vector = Vector2D.zero()
    with pytest.raises(ValueError):
        vector.normalized()


@pytest.mark.parametrize("a, b, expected",[
    (Vector2D(1,0), Vector2D(0,1), 0),
     (Vector2D(0,2), Vector2D(3,0), 0),
     (Vector2D(3,3), Vector2D(1,1), 6)
    ])
def test_dot_returns_direct_component_multiplication(a, b, expected):
    assert a.dot(b) == expected


@pytest.mark.parametrize("a, b, expected",[
    (Vector2D(1,0), Vector2D(0,1), 1),
     (Vector2D(0,2), Vector2D(3,0), -6),
     (Vector2D(3,3), Vector2D(1,1), 0)
    ])
def test_cross_returns_cross_multiplication(a, b, expected):
    assert a.cross(b) == expected

@pytest.mark.parametrize("magnitude, angle, expected_x, expected_y", [
    (2, 0, 2, 0),             # along +x
    (2, math.pi / 2, 0, 2),             # straight up
    (2, math.pi / 4, math.sqrt(2), math.sqrt(2)),  # 45 degrees: both parts equal, sqrt(2) each
    (3, math.pi, -3, 0),             # along -x
    (1, -math.pi / 2, 0, -1),             # straight down
])
def test_from_polar_converts_to_cartesian(magnitude, angle, expected_x, expected_y):
    result = Vector2D.from_polar(magnitude, angle)
    assert result.x == pytest.approx(expected_x, abs=1e-9)
    assert result.y == pytest.approx(expected_y, abs=1e-9)


@pytest.mark.parametrize("vector, expected",[
    (Vector2D(1, 0), 0,),
    (Vector2D(1, 1), math.pi/4),
    (Vector2D(0, 2), math.pi/2),
    (Vector2D(-1, 0), math.pi),
    (Vector2D(0, -1), -math.pi/2),
])
def test_angle(vector, expected):
    assert vector.angle() == pytest.approx(expected)

    

# Vector with vector: both operands must keep their original components
@pytest.mark.parametrize("op, ax, ay, bx, by", [
    (operator.add, 1, 2, 3, 4),
    (operator.sub, -1, 2, 0.5, -3),
])
def test_vector_operations_do_not_modify_operands(op, ax, ay, bx, by):
    a = Vector2D(ax, ay)
    b = Vector2D(bx, by)

    op(a, b)

    assert a.x == ax
    assert a.y == ay
    assert b.x == bx
    assert b.y == by


# Vector with number: the vector must keep its original components
@pytest.mark.parametrize("op, ax, ay, scalar", [
    (operator.mul, 1, 2, 3),
    (operator.truediv, 4, -6, 2),
])
def test_scalar_operations_do_not_modify_vector(op, ax, ay, scalar):
    a = Vector2D(ax, ay)

    op(a, scalar)

    assert a.x == ax
    assert a.y == ay


def test_negation_does_not_modify_vector():
    a = Vector2D(1, -2)

    -a

    assert a.x == 1
    assert a.y == -2


def test_zero_factory():
    z = Vector2D.zero()
    assert z.x == 0.0
    assert z.y == 0.0


@pytest.mark.parametrize("vector, expected", [
    (Vector2D(3,4), "(3.000, 4.000)"),
    (Vector2D(-1.23456, 0), "(-1.235, 0.000)")
])
def test_text_form(vector, expected):
    assert str(vector) == expected



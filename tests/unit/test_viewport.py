import pytest
from physlab.core.vector2d import Vector2D
from physlab.ui.viewport import Viewport

#--------------------------------------------AC1------------------------------------------------
@pytest.mark.parametrize("point, expected",[
    (Vector2D(0,0), (40, 560)),
    (Vector2D(1,1), (60, 540)),
    (Vector2D(-1,2), (20, 520))
])
def test_mapping(point, expected):
    viewport = Viewport(width_px=900, height_px=600)
    assert viewport.to_screen(point) == expected


#--------------------------------------------AC2------------------------------------------------

@pytest.mark.parametrize("point",[
    (Vector2D(0,0)),
    (Vector2D(3.5,2)),
    (Vector2D(-1,4)),
    (Vector2D(2,-3))
])
def test_inverse(point):
    viewport = Viewport(width_px=900, height_px=600)
    sx, sy = viewport.to_screen(point)

    world = viewport.to_world(sx, sy)
    assert world.x == pytest.approx(point.x, abs=1e-9)
    assert world.y == pytest.approx(point.y, abs=1e-9)

#--------------------------------------------AC3------------------------------------------------

@pytest.mark.parametrize("vector, s, expected",[
    (Vector2D(1,1), 10, (10, -10)),
    (Vector2D(0,-2), 5, (0, 10)),
])
def test_directions(vector, s, expected):
    viewport = Viewport(width_px=900, height_px=600)
    result = viewport.vector_to_screen(vector, s)
    assert result[0] == pytest.approx(expected[0])
    assert result[1] == pytest.approx(expected[1])

#--------------------------------------------AC4------------------------------------------------
@pytest.mark.parametrize("corner, expected", [
    (Vector2D(0,0), (40, 560)),
    (Vector2D(40,0), (860, 560)),
    (Vector2D(0,10), (40, 355)),
    (Vector2D(40,10), (860,355))
])
def test_fit(corner, expected):
    viewport = Viewport(width_px=900, height_px=600 )
    viewport.fit(0, 0, 40, 10)
    assert viewport.pixels_per_meter == pytest.approx(20.5)

    corner_screen = viewport.to_screen(corner)
    assert corner_screen[0] == pytest.approx(expected[0])
    assert corner_screen[1] == pytest.approx(expected[1])

@pytest.mark.parametrize("x_min, y_min, x_max, y_max",[
    (0,0,-40,10),
    (0,0,40,-10),
    (0,0,0,10)
])
def test_fit_validation(x_min, y_min, x_max, y_max):
    viewport = Viewport(width_px=900, height_px=600 )
    with pytest.raises(ValueError):
        viewport.fit(x_min, y_min, x_max, y_max)
    

#--------------------------------------------AC5------------------------------------------------

def test_constructor_validation():
    with pytest.raises(ValueError):
        Viewport(900, 600, pixels_per_meter=0)

    with pytest.raises(ValueError):
        Viewport(900, 600, pixels_per_meter=-1)





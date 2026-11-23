import pytest

from physlab.ui.renderer import Renderer
from tests.conftest import FakeRenderer



def test_abstract_renderer():
    with pytest.raises(TypeError):
        Renderer()

def test_double():
    renderer = FakeRenderer()

    assert renderer.size == (900, 600)
    assert renderer.calls == []

    renderer.draw_circle((0,0), 1.0, "#2e7d32")
    renderer.draw_line((0,0), (2,2), "#2e7d32")
    renderer.draw_line((0,0), (2,2), "#2e7d32", 2.0)
    renderer.draw_polyline([(0,0), (1,1), (3,3)], "#2e7d32")
    renderer.draw_arrow((0,0), (2,2), "#2e7d32")
    renderer.draw_text((0,0), "Test1", "#2e7d32")

    assert len(renderer.calls) == 6
    assert renderer.calls== [("draw_circle", (0,0), 1.0, "#2e7d32"),
                             ("draw_line",(0,0), (2,2), "#2e7d32", 1.0),
                             ("draw_line",(0,0), (2,2), "#2e7d32", 2.0),
                             ("draw_polyline", [(0,0), (1,1), (3,3)], "#2e7d32", 1.0),
                             ("draw_arrow", (0,0), (2,2), "#2e7d32", 2.0),
                             ("draw_text", (0,0), "Test1", "#2e7d32")]
    
    assert renderer.calls[2][-1] == 2.0 

    renderer.clear()

    assert renderer.calls[-1] == ("clear",)


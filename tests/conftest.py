from physlab.ui.renderer import Renderer

class FakeRenderer(Renderer):

    def __init__(self):
        self.calls = []
    @property
    def size(self):
        return (900, 600)


    def draw_circle(self, center, radius, fill):
        self.calls.append(("draw_circle", center, radius, fill))

    def draw_line(self, start, end, colour, width = 1.0):
        self.calls.append(("draw_line", start, end, colour, width))

    def draw_polyline(self, points, colour, width = 1.0):
        self.calls.append(("draw_polyline", points, colour, width))

    def draw_arrow(self, start, end, colour, width = 2.0):
        self.calls.append(("draw_arrow", start, end, colour, width))

    def draw_text(self, position, text, colour):
        self.calls.append(("draw_text", position, text, colour))

    def clear(self):
        self.calls.append(("clear",))

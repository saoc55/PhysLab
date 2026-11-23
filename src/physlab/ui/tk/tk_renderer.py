import tkinter as tk
from physlab.ui.renderer import Point, Renderer

class TkRenderer(Renderer):
    def __init__(self, canvas):
        self._canvas = canvas

    @property
    def size(self):
        width = self._canvas.cget("width")
        height = self._canvas.cget("height")
        return (int(width), int(height))

    def clear(self):
        self._canvas.delete("all")

    def draw_circle(self, center: Point, radius: float, fill: str):
        cx, cy = center
        top_left_corner = (cx - radius, cy - radius)
        bottom_right_corner = (cx + radius, cy + radius)

        x0, y0 = top_left_corner
        x1, y1 = bottom_right_corner

        self._canvas.create_oval(x0, y0, x1, y1, fill= fill, outline= "")
        
    def draw_line(self, start:Point, end: Point, colour: str, width: float = 1.0):
        x1, y1 = start
        x2, y2 = end
        self._canvas.create_line(x1, y1, x2, y2, fill = colour, width = width)

    def draw_polyline(self, points: list[Point], colour: str, width: float = 1.0):
        if len(points) < 2:
            return

        flat_coords = [coord for p in points for coord in p]
        self._canvas.create_line(*flat_coords, fill = colour, width = width)

    def draw_arrow(self, start: Point, end: Point, colour: str, width: float = 2.0):
        x1, y1 = start
        x2, y2 = end
        self._canvas.create_line(x1, y1, x2, y2, fill=colour, width=width, arrow=tk.LAST)

    def draw_text(self, position: Point, text: str, colour: str):
        x, y = position
        self._canvas.create_text(x, y, text= text, fill= colour, anchor=tk.NW, font=("Courier", 10))
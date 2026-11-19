from __future__ import annotations
from physlab.core.vector2d import Vector2D

class Viewport:
    def __init__(self, width_px: int, height_px: int, pixels_per_meter: float = 20.0, origin_px: tuple[float, float] = (40.0, 560.0)) -> None:

        if pixels_per_meter <= 0:
            raise ValueError("pixels per meter must be larger than 0")
        
        self.width_px = width_px
        self.height_px = height_px
        self.pixels_per_meter = pixels_per_meter
        self.origin_px = origin_px

    def to_screen(self, point: Vector2D) -> tuple[float, float]:
        o_x, o_y = self.origin_px[0], self.origin_px[1]
        s_x = o_x + (point.x * self.pixels_per_meter)
        s_y = o_y - (point.y * self.pixels_per_meter)
        return s_x, s_y

    def to_world(self, s_x: float, s_y: float) -> Vector2D:
        o_x, o_y = self.origin_px[0], self.origin_px[1]
        x = (s_x - o_x) / self.pixels_per_meter
        y = (o_y - s_y) / self.pixels_per_meter
        return Vector2D(x, y)

    def vector_to_screen(self, vector: Vector2D, px_per_unit: float) -> tuple[float, float]:
        return (vector.x * px_per_unit, -(vector.y * px_per_unit))

    def fit(self, x_min, y_min, x_max, y_max, margin_px: float = 40.0) -> None:
        if x_max <= x_min or y_max <= y_min:
            raise ValueError("Max values must be larger than min values")

        # pixels/meter
        c_x = (self.width_px - (2*margin_px)) / (x_max - x_min)
        c_y = (self.height_px - (2*margin_px)) / (y_max - y_min)
        self.pixels_per_meter = min(c_x, c_y)

        # Origin_px
        o_x = margin_px - (x_min * self.pixels_per_meter)
        o_y = (self.height_px - margin_px) + (y_min * self.pixels_per_meter)
        self.origin_px = (o_x, o_y)


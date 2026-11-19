from __future__ import annotations
from abc import ABC, abstractmethod 
from typing import TypeAlias, Final

Point: TypeAlias = tuple[float, float]

COLOUR_VELOCITY: Final[str] ="#2e7d32" #green
COLOUR_ACCELERATION: Final[str] = "#1565c0" #blue
COLOUR_NET_FORCE: Final[str] ="#c62828" #red
COLOUR_FORCE: Final[str]= "#8d6e63" #brown
COLOUR_BODY: Final[str] = "#3366cc"
COLOUR_TRAIL: Final[str]= "#9e9e9e"
COLOUR_GROUND: Final[str] = "#5d4037"
COLOUR_TEXT: Final[str]= "#000000"

class Renderer(ABC):

    @property
    @abstractmethod
    def size(self)-> tuple[int, int]:
        """Returns (width, height) in pixels, both ints."""
        

    @abstractmethod
    def clear(self) -> None:
        """Each subclass shall eraseeverything drawn so far."""
        

    @abstractmethod
    def draw_circle(self, center: Point, radius: float, fill: str) -> None:
        """Each subclass shall draw a circlefilled with colour fill ("#rrggbb"),with no outline, centred atcenter, radius in pixels"""
        

    @abstractmethod
    def draw_line(self, start:Point, end: Point, colour: str, width: float = 1.0) -> None:
        """Each subclass shall draw astraight line from start to end,width in pixels."""
        

    @abstractmethod
    def draw_polyline(self, points: list[Point], colour: str, width: float = 1.0) -> None:
        """Each subclass shall draw oneconnected line through all points,in order. With fewer than 2 pointsit shall draw nothing and notraise""" 
        

    @abstractmethod
    def draw_arrow(self, start: Point, end:Point, colour: str, width: float =2.0) -> None:
        """Each subclass shall draw a linefrom start to end with anarrowhead at end."""
        

    @abstractmethod
    def draw_text(self, position: Point, text:str, colour: str) -> None:
        """Each subclass shall write textwith its top left corner atposition."""
        


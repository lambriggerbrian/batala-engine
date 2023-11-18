from pathlib import Path
from dataclasses import dataclass
import random
import time
from typing import Callable
from numpy import array
import pygame
from semver import Version
from batala.components.ndarray_component_manager import (
    NdarrayComponent,
    NdarrayComponentManagerAPI,
)
from batala.components.transform2d_component_manager import (
    Transform2D,
)
from batala.engine.engine import Engine

from batala import PACKAGE_PATH
from batala.engine.engine import Engine
from batala.engine.loader import YamlLoader
from batala.engine.entity import Entity
from batala.engine.plugin import PluginAPI


test_config = Path(PACKAGE_PATH, "examples/configs/pygame.yaml")
WORLD_GRAVITY = 100


@dataclass(frozen=True)
class Size:
    width: int
    height: int


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int


@dataclass(frozen=True)
class Circle:
    radius: int
    color: Color


@dataclass()
class Transform:
    x: float
    y: float


class GameObject:
    transform: Transform
    circle: Circle

    def __init__(
        self,
        transform=Transform(0, 0),
        circle=Circle(5, Color(0, 0, 0)),
    ):
        self.transform = transform
        self.circle = circle

    def render(self, surface: pygame.Surface):
        color = (self.circle.color.r, self.circle.color.g, self.circle.color.b)
        position = (self.transform.x, self.transform.y)
        pygame.draw.circle(surface, color, position, self.circle.radius)


@dataclass(frozen=True)
class GameAPI(PluginAPI, version=Version(1, 0, 0)):
    create: Callable[[Entity, int, int], None]


class Game:
    running: bool
    engine: Engine
    component_manager: NdarrayComponentManagerAPI
    resolution: Size
    screen_color: Color
    objects: dict[Entity, GameObject]
    _screen: pygame.Surface

    def __init__(
        self,
        engine: Engine,
        resolution: Size = Size(500, 600),
        screen_color: Color = Color(255, 255, 255),
    ):
        self.running = False
        self.engine = engine
        self.component_manager = engine.component_managers["Transform2DPlugin"]  # type: ignore
        self.resolution = resolution
        self.screen_color = screen_color
        self.objects = {}
        self._screen = pygame.display.set_mode(
            (self.resolution.width, self.resolution.height)
        )

    def create(self, x: float = 0, y: float = 0):
        entity = self.engine.create_entity()
        x_velocity = random.random() * 100 - 50
        y_velocity = random.random() * 100 - 50
        component = NdarrayComponent(
            array((x, y, x_velocity, y_velocity, 0, WORLD_GRAVITY), dtype=Transform2D)
        )
        self.component_manager.register_component(entity)
        self.component_manager.assign_component(entity, component)
        self.objects[entity] = GameObject(transform=Transform(x, y))

    def handle_input(self):
        pass

    def handle_render(self):
        self._screen.fill(
            (self.screen_color.r, self.screen_color.g, self.screen_color.b)
        )
        for entity, game_object in self.objects.items():
            transform_instance = self.component_manager.get_component(entity)
            if transform_instance is not None:
                game_object.transform.x = float(transform_instance["x"])
                game_object.transform.y = float(transform_instance["y"])
            game_object.render(self._screen)
        pygame.display.flip()

    def step(self, delta_time: int):
        self.engine.step(delta_time)
        self.handle_render()


def main():
    loader = YamlLoader(test_config)
    config = loader.load()
    loader.import_modules()
    engine = Engine.from_config(config)
    game = Game(engine)
    for i in range(50):
        game.create(i * 10.0 + 5, i * 10.0)
    last_frame = time.time_ns()
    for i in range(5000):
        current = time.time_ns()
        game.step(current - last_frame)
        last_frame = current


if __name__ == "__main__":
    main()

from dataclasses import dataclass
from typing import Callable
import pygame
from semver import Version
from batala.engine.engine import Engine

from batala.engine.entity import Entity
from batala.engine.plugin import Plugin, PluginAPI
from batala.engine.utils import Registry
from batala.systems.system import System, SystemAPI


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


@dataclass(frozen=True)
class Transform2D:
    x: int
    y: int


class GameObject:
    transform: Transform2D
    circle: Circle

    def __init__(
        self,
        transform=Transform2D(0, 0),
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


class Game(System):
    running: bool
    resolution: Size
    screen_color: Color
    objects: dict[Entity, GameObject]
    _screen: pygame.Surface
    _engine: Engine

    def __init__(
        self,
        resolution: Size = Size(500, 500),
        screen_color: Color = Color(255, 255, 255),
    ):
        self.running = False
        self.resolution = resolution
        self.screen_color = screen_color
        self.objects = {}
        self._screen = pygame.display.set_mode(
            (self.resolution.width, self.resolution.height)
        )

    def create(self, entity: Entity, x: int = 0, y: int = 0):
        self.objects[entity] = GameObject(transform=Transform2D(x, y))

    def handle_input(self):
        pass
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         match event.key:
        #             case pygame.K_ESCAPE:
        #                 self.running = False
        #             case pygame.K_DOWN:
        #                 self.kinematic2D_manager.update_component(
        #                     self.player, "velocity", (0, 1)
        #                 )
        #             # case pygame.locals.K_UP:
        #             #     self.objects[0].transform.velocity.y -= 1
        #             # case pygame.locals.K_DOWN:
        #             #     self.objects[0].transform.velocity.y += 1
        #             # case pygame.locals.K_LEFT:
        #             #     self.objects[0].transform.velocity.x -= 1
        #             # case pygame.locals.K_RIGHT:
        #             #     self.objects[0].transform.velocity.x += 1
        #             case _:
        #                 pass
        #     if event.type == KEYUP:
        #         match event.key:
        #             case pygame.locals.K_DOWN:
        #                 self.kinematic2D_manager.update_component(
        #                     self.player, "velocity", (0, 0)
        #                 )
        #             # case pygame.locals.K_UP | pygame.locals.K_DOWN:
        #             #     self.objects[0].transform.velocity.y = 0
        #             # case pygame.locals.K_LEFT | pygame.locals.K_RIGHT:
        #             #     self.objects[0].transform.velocity.x = 0
        #             case _:
        #                 pass
        #     elif event.type == pygame.QUIT:
        #         self.running = False

    def handle_render(self):
        self._screen.fill(
            (self.screen_color.r, self.screen_color.g, self.screen_color.b)
        )
        for entity, game_object in self.objects.items():
            # transform_instance = self.transform_manager.get_component(entity)
            # if transform_instance is not None:
            #     game_object.transform = transform_instance["transform"]
            game_object.render(self._screen)
        pygame.display.flip()

    def get_dependencies(self, plugins: Registry[Plugin]):
        pass

    def step(self, delta_time: int):
        self.handle_render()


class GamePlugin(Plugin, version=Version(1, 0, 0)):
    def __init__(self) -> None:
        self.game = Game()
        self.implemented_apis = Registry(
            {
                "GameAPI": GameAPI(create=self.game.create),
                "SystemAPI": SystemAPI(
                    get_dependencies=self.game.get_dependencies, step=self.game.step
                ),
            }
        )

from pathlib import Path

from batala import PACKAGE_PATH
from batala.engine.engine import Engine
from batala.engine.loader import YamlLoader

test_config = Path(PACKAGE_PATH, "examples/configs/pygame.yaml")


def main():
    loader = YamlLoader(test_config)
    config = loader.load()
    loader.import_modules()
    engine = Engine.from_config(config)
    game_api = engine.apis["GamePlugin"]["GameAPI"]
    for i in range(50):
        position = (i * 10) + 5
        entity = engine.create_entity()
        game_api.create(entity, position, position)  # type: ignore
    for i in range(10000):
        engine.step(0)


if __name__ == "__main__":
    main()

from batala.engine import MINIMUM_FREE_INDICES
from batala.engine.entity import Entity
from batala.engine.entity_manager import EntityManager


def test_init():
    entity_manager = EntityManager()
    assert entity_manager is not None
    assert isinstance(entity_manager, EntityManager)


def test_create():
    entity_manager = EntityManager()
    entity = entity_manager.create()
    assert entity is not None
    assert isinstance(entity, Entity)


def test_is_alive():
    entity_manager = EntityManager()
    entity_alive = entity_manager.create()
    assert entity_manager.is_alive(entity_alive)


def test_destroy():
    entity_manager = EntityManager()
    entity_dead = entity_manager.create()
    entity_manager.destroy(entity_dead)
    assert not entity_manager.is_alive(entity_dead)


def test_count():
    entity_manager = EntityManager()
    entity = entity_manager.create()
    assert entity_manager.count == 1
    entity_manager.destroy(entity)
    assert entity_manager.count == 0
    for i in range(10):
        entity_manager.create()
        assert entity_manager.count == i+1


def test_index_recycling():
    entity_manager = EntityManager()
    entities = []
    for i in range(MINIMUM_FREE_INDICES*2):
        entities.append(entity_manager.create())
    for j in range(MINIMUM_FREE_INDICES+1):
        entity = entities.pop()
        entity_manager.destroy(entity)
    entity_recycled = entity_manager.create()
    assert entity_recycled.generation == 1

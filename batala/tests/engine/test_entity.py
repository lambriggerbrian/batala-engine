from batala.engine import Generation, Id, Index
from batala.engine.entity import Entity

zero_id = Id(0)


def test_init():
    entity = Entity(Index(0), Generation(0))
    assert entity is not None
    assert isinstance(entity, Entity)


def test_id():
    entity = Entity(id=zero_id)
    assert entity.id == zero_id


def test_index():
    entity = Entity(Index(1), Generation(0))
    assert entity.index == Index(1)


def test_generation():
    entity = Entity(Index(1), Generation(1))
    assert entity.generation == Generation(1)


def test_generate_id():
    id = Entity.generate_id(Index(0), Generation(0))
    assert id == zero_id


def test_get_index():
    id = Entity.generate_id(Index(1), Generation(1))
    assert Entity.get_index(id) == Index(1)


def test_get_generation():
    id = Entity.generate_id(Index(2), Generation(2))
    assert Entity.get_generation(id) == Generation(2)


def test_hash():
    entity = Entity(Index(0), Generation(0))
    assert entity.__hash__() == zero_id


def test_equals():
    entity_zero = Entity(Index(0), Generation(0))
    entity_one = Entity(Index(1), Generation(0))
    entity_zero_one = Entity(Index(0), Generation(1))
    entity_zero_duplicate = Entity(Index(0), Generation(0))
    assert entity_zero == entity_zero
    assert not entity_zero == entity_one
    assert not entity_zero == entity_zero_one
    assert entity_zero == entity_zero_duplicate

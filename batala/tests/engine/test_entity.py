import pytest
from batala.engine import Generation, Id, Index
from batala.engine.entity import Entity

zero_id = Id(0)


def test_init():
    entity = Entity(0, 0)
    assert entity is not None
    assert isinstance(entity, Entity)


def test_id():
    entity = Entity(id=zero_id)
    assert entity.id == zero_id


def test_index():
    entity = Entity(1, 0)
    assert entity.index == Index(1)


def test_generation():
    entity = Entity(1, 1)
    assert entity.generation == Generation(1)


def test_generate_id():
    id = Entity.generate_id(0, 0)
    assert id == zero_id


def test_get_index():
    id = Entity.generate_id(1, 1)
    assert Entity.get_index(id) == Index(1)


def test_get_generation():
    id = Entity.generate_id(2, 2)
    assert Entity.get_generation(id) == Generation(2)


def test_hash():
    entity = Entity(0, 0)
    assert entity.__hash__() == zero_id


def test_equals():
    entity_zero = Entity(0, 0)
    entity_one = Entity(1, 0)
    entity_zero_one = Entity(0, 1)
    entity_zero_duplicate = Entity(0, 0)
    assert entity_zero == entity_zero
    assert not entity_zero == entity_one
    assert not entity_zero == entity_zero_one
    assert entity_zero == entity_zero_duplicate

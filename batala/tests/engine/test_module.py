from semver import Version
from batala.engine import ModuleId
from batala.engine.module import ModuleType, generate_moduleId
from batala.tests.engine.mock import TestModule


def test_name():
    module = TestModule()
    assert module.get_info("name") == "Test"


def test_version():
    module = TestModule()
    version = module.get_info("version")
    assert version == Version(1, 0, 0)
    assert version > Version(0, 0, 0)
    assert version < Version(1, 0, 1)


def test_type():
    module = TestModule()
    type = module.get_info("type")
    assert type == ModuleType.SYSTEM
    assert type != ModuleType.COMPONENT
    assert type != ModuleType.ENTITY
    assert type != ModuleType.GROUP


def test_moduleId():
    module = TestModule()
    name = module.get_info("name")
    version = module.get_info("version")
    moduleId = module.get_info("moduleId")
    generated_id = generate_moduleId(name, version)
    assert moduleId == generated_id

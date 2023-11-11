from batala.examples.classes.component_examples import TestComponent


def test_init():
    component = TestComponent()
    assert component is not None
    assert isinstance(component, TestComponent)


def test_getitem():
    component = TestComponent()
    assert component["discrete_steps"] == 0
    assert component["continuous_time"] == 0


def test_setitem():
    component = TestComponent()
    component["discrete_steps"] = 1
    component["continuous_time"] = 60
    assert component["discrete_steps"] == 1
    assert component["continuous_time"] == 60

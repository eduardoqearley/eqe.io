from src.openspec_core.generator import CodeGenerator
from src.openspec_core.models import Requirement, Scenario


def make_req():
    sc = Scenario(title="Example scenario", given=["Given x"], when=["When y"], then=["Then z"])
    req = Requirement(title="Do Something", description="Do something important", section="ADDED", scenarios=[sc])
    return req, sc


def test_render_function():
    gen = CodeGenerator()
    req, sc = make_req()
    out = gen.render_function(req)
    assert "def do_something" in out
    assert "Do something important" in out
    assert "pass" in out


def test_render_test():
    gen = CodeGenerator()
    req, sc = make_req()
    out = gen.render_test(sc)
    assert "def test_example_scenario" in out
    assert "Given x" in out
    assert "assert True" in out

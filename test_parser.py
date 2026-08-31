import pytest
from pathlib import Path
from src.openspec_core.parser import SpecParser
from src.openspec_core.models import Scenario, Requirement, CapabilitySpec


class TestSpecParser:
    """Test parsing OpenSpec .md files."""

    def test_parse_title_and_description(self):
        """Test extracting title and description."""
        spec_dir = Path("openspec/changes/demo/specs/python-spec-parser")
        parser = SpecParser(str(spec_dir.parent))
        spec = parser.parse(spec_dir / "spec.md")
        
        assert spec.name == "Python Spec Parser"
        assert "Parse OpenSpec" in spec.description

    def test_parse_sections(self):
        """Test extracting ADDED/MODIFIED sections."""
        spec_dir = Path("openspec/changes/demo/specs/python-spec-parser")
        parser = SpecParser(str(spec_dir.parent))
        spec = parser.parse(spec_dir / "spec.md")
        
        assert len(spec.requirements) > 0
        for req in spec.requirements.values():
            assert req.section in ["ADDED", "MODIFIED", "REMOVED", "RENAMED"]

    def test_parse_requirements(self):
        """Test extracting requirements (### Requirement:)."""
        spec_dir = Path("openspec/changes/demo/specs/python-spec-parser")
        parser = SpecParser(str(spec_dir.parent))
        spec = parser.parse(spec_dir / "spec.md")
        
        assert len(spec.requirements) > 0
        for title, req in spec.requirements.items():
            assert isinstance(req, Requirement)
            assert len(req.title) > 0
            assert len(req.description) > 0

    def test_parse_scenarios(self):
        """Test extracting scenarios with Given/When/Then."""
        spec_dir = Path("openspec/changes/demo/specs/python-spec-parser")
        parser = SpecParser(str(spec_dir.parent))
        spec = parser.parse(spec_dir / "spec.md")
        
        for req in spec.requirements.values():
            assert len(req.scenarios) > 0
            for scenario in req.scenarios:
                assert isinstance(scenario, Scenario)
                assert len(scenario.title) > 0
                # Each scenario should have given/when/then
                assert len(scenario.given) > 0 or len(scenario.when) > 0 or len(scenario.then) > 0

    def test_parse_all_specs(self):
        """Test parsing all specs in directory."""
        parser = SpecParser("openspec/changes/demo/specs")
        specs = parser.parse_all()
        
        # Should find 5 capability specs
        assert len(specs) == 5
        assert "python-spec-parser" in specs
        assert "python-code-generator" in specs
        assert "externalized-config" in specs
        assert "python-validator" in specs
        assert "llm-spec-writer" in specs

    def test_scenario_serialization(self):
        """Test Scenario can be serialized."""
        scenario = Scenario(
            title="Test scenario",
            given=["Given step 1"],
            when=["When step 1"],
            then=["Then step 1"]
        )
        scenario_dict = scenario.to_dict()
        assert scenario_dict["title"] == "Test scenario"
        assert "given" in scenario_dict

    def test_requirement_serialization(self):
        """Test Requirement can be serialized."""
        req = Requirement(
            title="Test requirement",
            description="Test description",
            section="ADDED",
            scenarios=[]
        )
        req_dict = req.to_dict()
        assert req_dict["title"] == "Test requirement"
        assert req_dict["section"] == "ADDED"

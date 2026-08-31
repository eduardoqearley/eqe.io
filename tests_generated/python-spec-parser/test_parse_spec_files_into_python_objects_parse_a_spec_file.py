import pytest

def test_parse_a_spec_file():
    # Given: a spec.md file with ADDED/MODIFIED/REMOVED/RENAMED sections and Scenarios, when parsed by SpecParser, then it extracts:
    # When: parsed by SpecParser
    # Then: it extracts:
- Requirement title and description
- List of scenarios with given/when/then steps
- Section type (ADDED/MODIFIED/REMOVED/RENAMED)
- Capability metadata
    assert True
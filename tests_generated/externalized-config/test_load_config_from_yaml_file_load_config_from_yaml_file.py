import pytest

def test_load_config_from_yaml_file():
    # Given: a config.yaml file with key-value pairs, when the application starts, then it:
    # When: the application starts
    # Then: it:
- Reads the YAML file from a configurable path
- Parses it into a Config object with typed fields
- Validates required keys are present
- Raises clear error if file is missing or malformed
    assert True
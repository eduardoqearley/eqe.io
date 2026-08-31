import pytest
import os
import tempfile
from pathlib import Path
from src.openspec_core.config import AppConfig


class TestConfigLoading:
    """Test YAML config loading and validation."""

    def test_load_default_config(self):
        """Test loading config with defaults."""
        config = AppConfig()
        assert config.database.host == "localhost"
        assert config.database.port == 5432
        assert config.logging.level == "INFO"

    def test_load_config_from_yaml(self):
        """Test loading config from YAML file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_file.write_text("""
database:
  host: postgres.example.com
  port: 3306
  name: production_db

logging:
  level: DEBUG
""")
            config = AppConfig.load(str(config_file))
            assert config.database.host == "postgres.example.com"
            assert config.database.port == 3306
            assert config.database.name == "production_db"
            assert config.logging.level == "DEBUG"

    def test_env_var_override(self):
        """Test environment variable overrides YAML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.yaml"
            config_file.write_text("""
database:
  host: localhost
  port: 5432
""")
            # Set env vars
            os.environ["APP_DATABASE__HOST"] = "override.example.com"
            os.environ["APP_DATABASE__PORT"] = "9999"
            
            config = AppConfig.load(str(config_file))
            
            assert config.database.host == "override.example.com"
            assert config.database.port == 9999
            
            # Cleanup
            del os.environ["APP_DATABASE__HOST"]
            del os.environ["APP_DATABASE__PORT"]

    def test_env_var_precedence(self):
        """Test precedence: env vars > YAML > defaults."""
        # Env var overrides default
        os.environ["APP_LOGGING__LEVEL"] = "CRITICAL"
        config = AppConfig.load()  # Must call load() to apply env vars
        assert config.logging.level == "CRITICAL"
        del os.environ["APP_LOGGING__LEVEL"]

    def test_missing_config_file(self):
        """Test loading when config file doesn't exist."""
        config = AppConfig.load("/nonexistent/config.yaml")
        # Should use defaults
        assert config.database.host == "localhost"

    def test_config_serialization(self):
        """Test config can be serialized to dict."""
        config = AppConfig()
        config_dict = config.to_dict()
        assert "database" in config_dict
        assert "logging" in config_dict
        assert config_dict["database"]["host"] == "localhost"

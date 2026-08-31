from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import yaml
import os


class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "demo_db"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    format: str = "text"


class GeneratorConfig(BaseModel):
    output_dir: str = "src/"
    template_dir: str = "src/openspec_core/templates"


class ValidatorConfig(BaseModel):
    check_docstrings: bool = True
    check_type_hints: bool = True
    require_tests: bool = True


class AppConfig(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    generator: GeneratorConfig = Field(default_factory=GeneratorConfig)
    validator: ValidatorConfig = Field(default_factory=ValidatorConfig)

    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "AppConfig":
        """
        Load config from YAML file with environment variable overrides.
        
        Precedence: env vars (APP_*) > YAML > defaults
        """
        config_data = {}
        
        # Load YAML if it exists
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
        
        # Override with environment variables (APP_* prefix)
        for key, value in os.environ.items():
            if key.startswith("APP_"):
                # APP_DATABASE__HOST -> database.host
                parts = key[4:].lower().split("__")
                if len(parts) == 2:
                    section, field = parts
                    if section not in config_data:
                        config_data[section] = {}
                    config_data[section][field] = value
        
        return cls(**config_data)

    def to_dict(self) -> dict:
        return self.model_dump()

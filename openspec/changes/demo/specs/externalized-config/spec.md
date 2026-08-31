# Externalized Config

Load application configuration from YAML files (Kubernetes ConfigMap style) instead of hardcoding or using environment variables.

## ADDED Requirements

### Requirement: Load config from YAML file

Support external YAML config files that can be mounted, swapped, or versioned independently of code.

#### Scenario: Load config from YAML file
Given a config.yaml file with key-value pairs, when the application starts, then it:
- Reads the YAML file from a configurable path
- Parses it into a Config object with typed fields
- Validates required keys are present
- Raises clear error if file is missing or malformed

### Requirement: Override config with environment variables

Allow environment variables to override YAML values.

#### Scenario: Override config with environment variables
Given a config.yaml and environment variables prefixed with APP_, when loaded, then:
- YAML values are loaded first
- Environment variables override YAML values
- Precedence is clear: env vars > YAML > defaults
- Logging shows which values came from which source

### Requirement: Support config sections

Enable nested configuration structures with type safety.

#### Scenario: Support config sections
Given a config.yaml with nested sections (e.g. database, logging, features), when accessed, then:
- Sections are available as nested objects (config.database.host, config.logging.level)
- Type hints provide IDE autocomplete
- Missing optional sections don't cause errors

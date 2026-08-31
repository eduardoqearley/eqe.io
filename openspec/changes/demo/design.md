## Design

### Architecture Overview

```
OpenSpec Spec Files (YAML/Markdown)
          ↓
    SpecParser (Python)
          ↓
    Spec Data Model (Pydantic dataclasses)
          ↓
    CodeGenerator (Jinja2 templates)
          ↓
    Generated Python code + tests
          ↓
    Validator (Python introspection)
          ↓
    Coverage report + validation results
```

### Key Components

#### 1. Spec Parser (Python)
- **Purpose**: Read OpenSpec `.md` files and extract structured data
- **Technology**: Python regex + Pydantic models
- **Input**: `specs/*/spec.md` files
- **Output**: Python dataclass instances with requirements and scenarios
- **No LLM needed** — pure deterministic parsing

```python
# Example model structure
class Scenario:
    title: str
    given: List[str]
    when: List[str]
    then: List[str]

class Requirement:
    title: str
    description: str
    section: str  # ADDED, MODIFIED, REMOVED, RENAMED
    scenarios: List[Scenario]

class CapabilitySpec:
    name: str
    description: str
    requirements: Dict[str, Requirement]
```

#### 2. Code Generator (Jinja2 + Python)
- **Purpose**: Generate Python boilerplate from parsed specs
- **Technology**: Jinja2 templates + Python string generation
- **Inputs**: Parsed CapabilitySpec objects
- **Outputs**: `.py` source files and `test_*.py` files
- **Templates**: One per artifact type (function stubs, test stubs, config classes)
- **No LLM needed** — pure template expansion

**Jinja2 Template Example** (`templates/function_stub.j2`):
```jinja2
def {{ requirement.title | snake_case }}({% for param in requirement.get_params() %}{{ param }}{% if not loop.last %}, {% endif %}{% endfor %}) -> Any:
    """{{ requirement.description }}"""
    pass
```

**Test Template** (`templates/test_stub.j2`):
```jinja2
def test_{{ scenario.title | snake_case }}():
    # Given: {{ scenario.given | join(", ") }}
    # When: {{ scenario.when | join(", ") }}
    # Then: {{ scenario.then | join(", ") }}
    pass
```

#### 3. Config Loader (Pydantic + Python)
- **Purpose**: Load YAML config (Kubernetes ConfigMap style) with env var overrides
- **Technology**: PyYAML + Pydantic for validation
- **Input**: `config.yaml` file + environment variables (APP_*)
- **Output**: Typed Config object with nested sections
- **No LLM needed** — pure deterministic loading and validation

```python
# config.yaml
database:
  host: localhost
  port: 5432
  name: demo_db

logging:
  level: INFO
  format: json

# Generated config class
class DatabaseConfig:
    host: str
    port: int
    name: str

class LoggingConfig:
    level: str
    format: str

class AppConfig:
    database: DatabaseConfig
    logging: LoggingConfig
    
    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "AppConfig":
        # Load YAML → override with env vars → validate → return
        pass
```

#### 4. Validator (Python Introspection)
- **Purpose**: Check generated code against spec contracts
- **Technology**: Python `inspect` module + pytest discovery
- **Inputs**: Generated `.py` files + parsed spec
- **Outputs**: Validation report (JSON/Markdown)
- **Checks**:
  - Function exists, is callable, has correct signature
  - Docstrings match requirement descriptions
  - Tests exist for each requirement and scenario
  - Test names follow convention
- **No LLM needed** — pure static analysis

#### 5. LLM Integration Point
- **Purpose**: Write high-quality spec.md files
- **When**: User needs to create or improve specs
- **How**: LLM generates initial spec structure → human review → validate → use for code gen
- **Tool**: OpenAI API or compatible LLM service (configured via config.yaml)

### File Structure

```
openspec/
├── .openspec.yaml              # Root config
├── specs/
│   ├── python-spec-parser/
│   │   └── spec.md
│   ├── python-code-generator/
│   │   └── spec.md
│   ├── externalized-config/
│   │   └── spec.md
│   ├── python-validator/
│   │   └── spec.md
│   └── llm-spec-writer/
│       └── spec.md
├── changes/
│   └── demo/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       ├── .openspec.yaml
│       └── specs/
│           └── */{spec.md}  (copied from above during generation)
│
# Generated artifacts (after tasks completed)
src/
├── openspec_core/
│   ├── __init__.py
│   ├── models.py             # Pydantic dataclasses
│   ├── parser.py             # SpecParser class
│   ├── generator.py          # CodeGenerator class
│   ├── validator.py          # Validator class
│   ├── config.py             # ConfigLoader class
│   └── templates/
│       ├── function_stub.j2
│       ├── test_stub.j2
│       ├── config_class.j2
│       └── ...
├── demo_feature/
│   ├── __init__.py
│   ├── parser.py             # Generated from python-spec-parser spec
│   └── test_parser.py        # Generated tests
├── config.yaml               # Example config file
└── ...
```

### Implementation Strategy

1. **Deterministic first**: All code generation, parsing, validation happens in pure Python
2. **Jinja2 for templates**: Flexible, safe template language for code generation
3. **Pydantic for types**: Validation + IDE autocomplete + serialization
4. **LLM only for specs**: Use AI to write spec.md files, everything else is code-driven
5. **Config externalization**: All settings in `config.yaml`, mounted in k8s, no hardcoding

### Dependencies

```
pydantic>=2.0          # Data validation + typed models
pyyaml>=6.0            # Parse config.yaml
jinja2>=3.0            # Template code generation
pytest>=7.0            # Test framework
python-dotenv>=0.19    # Load env vars
openai>=1.0            # Optional: LLM integration for spec generation
```

### Data Flow Example

1. User writes or LLM generates `specs/python-spec-parser/spec.md`
2. SpecParser reads file → extracts requirements/scenarios → returns Requirement objects
3. CodeGenerator renders `templates/function_stub.j2` with Requirement data → generates `.py` files
4. CodeGenerator renders `templates/test_stub.j2` with Scenario data → generates `test_*.py` files
5. Validator introspects generated code → compares against spec requirements → reports coverage
6. All config loaded from `config.yaml` with env var overrides

### Configuration Example

```yaml
# config.yaml
generator:
  output_dir: src/
  template_dir: openspec_core/templates
  
parser:
  spec_dir: openspec/specs
  
validator:
  check_docstrings: true
  check_type_hints: true
  require_tests: true
  
llm:
  enabled: false
  # enabled: true
  # provider: openai
  # model: gpt-4
  # api_key: ${LLM_API_KEY}  # From env var
  
logging:
  level: INFO
  format: json
```

Environment variables override:
```bash
APP_GENERATOR__OUTPUT_DIR=/output
APP_LLM__ENABLED=true
APP_LOGGING__LEVEL=DEBUG
```

### Testing Strategy

- Unit tests for SpecParser (parsing markdown → correct data model)
- Unit tests for CodeGenerator (template rendering → valid Python)
- Unit tests for ConfigLoader (YAML + env var precedence)
- Integration tests (spec → code → validation roundtrip)
- No tests needed for LLM output (human review is the validation)

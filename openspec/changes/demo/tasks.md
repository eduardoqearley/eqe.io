## 1. Project Setup

- [ ] 1.1 Create `src/openspec_core/` package structure with `__init__.py` and verify directory hierarchy exists
- [ ] 1.2 Create `src/demo_feature/` package and verify files are present
- [ ] 1.3 Add dependencies to `requirements.txt` (pydantic, pyyaml, jinja2, pytest, python-dotenv) and verify `pip install -r requirements.txt` succeeds
- [ ] 1.4 Create `config.yaml` with example database, logging, and generator settings, and verify file loads without YAML errors

## 2. Data Models (Pydantic)

- [ ] 2.1 Create `src/openspec_core/models.py` with Pydantic dataclasses: `Scenario`, `Requirement`, `CapabilitySpec`, and verify models can be instantiated with test data
- [ ] 2.2 Add model serialization methods (to_dict, to_json) and verify JSON output is valid
- [ ] 2.3 Create `src/openspec_core/config.py` with `DatabaseConfig`, `LoggingConfig`, `GeneratorConfig`, `AppConfig` classes, and verify they accept nested YAML data

## 3. Config Loader

- [ ] 3.1 Implement `AppConfig.load(config_path: str)` in `src/openspec_core/config.py` to read YAML and parse into typed config, and verify `AppConfig.load("config.yaml")` returns AppConfig instance
- [ ] 3.2 Add environment variable override support (APP_* prefix) to config loader and verify env vars override YAML values with precedence: env > yaml > defaults
- [ ] 3.3 Create `test_config.py` with tests for YAML loading, env var override, missing required keys, and verify all tests pass with `pytest test_config.py`

## 4. Spec Parser

- [ ] 4.1 Implement `SpecParser` class in `src/openspec_core/parser.py` to read spec.md files and extract sections (ADDED/MODIFIED/REMOVED/RENAMED), and verify parsing one of the demo specs produces correct section data
- [ ] 4.2 Implement requirement parsing (### Requirement: header) and scenario extraction (#### Scenario: blocks with Given/When/Then), and verify `parser.parse()` returns Requirement objects with all scenarios
- [ ] 4.3 Implement `parse_all()` to traverse `openspec/specs/*/spec.md` and return dict of CapabilitySpec objects, and verify `parser.parse_all()` finds all 5 demo specs
- [ ] 4.4 Create `test_parser.py` with tests for parsing each section type, extracting scenarios, handling malformed markdown, and verify all tests pass

## 5. Jinja2 Templates

- [ ] 5.1 Create `src/openspec_core/templates/function_stub.j2` template to generate Python function stubs from Requirements with signature, docstring, and pass, and verify template renders without errors
- [ ] 5.2 Create `src/openspec_core/templates/test_stub.j2` template to generate pytest test functions from Scenarios with given/when/then sections as comments, and verify template renders valid Python
- [ ] 5.3 Create `src/openspec_core/templates/config_class.j2` template to generate Pydantic Config dataclasses from nested YAML structure, and verify template produces valid Python with nested models
- [ ] 5.4 Add Jinja2 filters (snake_case, title_case) to template environment and verify filters transform strings correctly

## 6. Code Generator

- [ ] 6.1 Implement `CodeGenerator` class in `src/openspec_core/generator.py` with `generate_functions()` method that renders function_stub.j2 for each requirement, and verify output is valid Python
- [ ] 6.2 Implement `generate_tests()` method that renders test_stub.j2 for each scenario and write to test_*.py files, and verify generated tests can be collected by pytest
- [ ] 6.3 Implement `generate_config_class()` method using config_class.j2 to auto-generate AppConfig class from config.yaml structure, and verify generated class matches handwritten Pydantic model
- [ ] 6.4 Implement full workflow: parse specs → generate code → write to output_dir specified in config.yaml, and verify generated files exist in correct locations

## 7. Validator

- [ ] 7.1 Implement `Validator` class in `src/openspec_core/validator.py` with `validate_signatures()` method that checks generated functions match requirement parameters using Python introspection, and verify validation passes for code generator output
- [ ] 7.2 Implement `check_docstrings()` to ensure generated functions have docstrings matching requirement descriptions, and verify validation reports missing docstrings
- [ ] 7.3 Implement `check_test_coverage()` to verify each requirement has at least one test and each scenario is covered, and verify validation report lists coverage by requirement
- [ ] 7.4 Implement `generate_report()` to output JSON and Markdown validation reports showing coverage %, missing tests, signature mismatches, and verify reports are readable and actionable
- [ ] 7.5 Create `test_validator.py` with tests for signature validation, docstring checks, coverage analysis, and verify all tests pass

## 8. Integration & Workflow

- [ ] 8.1 Create `src/openspec_core/cli.py` with workflow command: parse specs → generate code → validate → output report, and verify workflow runs end-to-end with `python cli.py`
- [ ] 8.2 Implement progress output showing "Parsing X specs... Generating code... Validating... Done" with clear status, and verify user sees progress
- [ ] 8.3 Create `demo_feature/` implementation files generated from demo specs and verify generated code is valid Python that imports without errors
- [ ] 8.4 Create README.md documenting the hybrid Python+Jinja2 workflow, config.yaml format, CLI usage, and verification steps, and verify README is clear and complete

## 9. Demo & Validation

- [ ] 9.1 Run full workflow on demo specs and verify all 5 capabilities generate code successfully
- [ ] 9.2 Execute generated tests (pytest) and verify they pass (placeholder tests should pass with pass statements)
- [ ] 9.3 Run validator on generated code and verify coverage report shows 100% requirement coverage and 100% scenario coverage
- [ ] 9.4 Test config loading with both config.yaml and environment variable overrides and verify both methods work and env vars take precedence
- [ ] 9.5 Create example config.yaml for k8s ConfigMap mounting and document how to deploy with different configs for dev/staging/prod, and verify documentation is deployment-ready

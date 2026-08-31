# Python Validator

Validate generated code against spec requirements to catch regressions early.

## ADDED Requirements

### Requirement: Validate function signatures

Run automated checks on generated code to ensure it matches spec contracts.

#### Scenario: Validate function signatures
Given a spec requirement and generated function, when validated, then it checks:
- Function exists and is callable
- Parameters match scenario given/when steps
- Return type hints are present
- Docstring is populated from spec

### Requirement: Validate test coverage

Ensure generated tests cover all requirements and scenarios.

#### Scenario: Validate test coverage
Given generated tests, when validated, then it confirms:
- Each requirement has at least one test
- Each scenario is covered by a test
- Test names follow naming convention
- Test assertions reference scenario then-steps

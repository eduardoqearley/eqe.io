## Why

Deterministic code is faster, more reliable, and cheaper than LLM calls. This demo showcases a hybrid approach: use Python for structured, repeatable tasks (parsing, validation, code generation, file operations) and reserve LLM calls for tasks that require creativity, reasoning, or human judgment. This maximizes efficiency and reduces costs while maintaining quality.

## What Changes

- Add Python-first tooling to the OpenSpec workflow
- Integrate deterministic code generation where possible (scaffolding, boilerplate, formatting)
- Use LLM strategically only for spec writing, design review, and complex reasoning
- Demonstrate parsing specs → generating code automatically
- Show how Python can validate requirements before LLM involvement

## Capabilities

### New Capabilities
- `python-spec-parser`: Parse specs and extract structured requirements into Python objects
- `python-code-generator`: Auto-generate boilerplate code from specs using deterministic templates
- `python-validator`: Validate generated code against spec requirements
- `externalized-config`: Load application config from YAML files (Kubernetes-style ConfigMaps)
- `llm-spec-writer`: Use LLM only for writing high-quality, well-reasoned specs (non-deterministic)

### Modified Capabilities
(none)

## Impact

- Reduces LLM token usage by handling deterministic work in Python
- Faster iteration cycles with instant code generation
- Better type safety and structure through Python dataclasses/Pydantic
- LLM stays focused on reasoning and quality writing, not mechanical tasks

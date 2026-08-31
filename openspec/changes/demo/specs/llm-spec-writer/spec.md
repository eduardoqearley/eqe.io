# LLM Spec Writer

Use LLM to write clear, comprehensive specs with well-reasoned scenarios—the creative work that benefits from AI reasoning.

## ADDED Requirements

### Requirement: Generate spec from feature description

LLM assists in spec authoring for creative, well-reasoned requirements.

#### Scenario: Generate spec from feature description
Given a feature description and requirements from a human, when LLM generates a spec, then it:
- Creates a clear, well-structured spec.md file
- Writes ADDED/MODIFIED/REMOVED/RENAMED sections as needed
- Generates realistic Scenarios with Given/When/Then steps
- Follows OpenSpec conventions and naming

### Requirement: Review and enhance existing spec

Improve incomplete specs with better scenarios and edge cases.

#### Scenario: Review and enhance existing spec
Given a draft spec with minimal details, when LLM reviews it, then it:
- Identifies missing scenarios or edge cases
- Suggests improvements to requirement wording
- Adds realistic Given/When/Then examples
- Proposes missing capabilities that logically follow

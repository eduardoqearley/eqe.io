from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Scenario:
    """Represents a Given-When-Then scenario from a spec."""
    title: str
    given: List[str]
    when: List[str]
    then: List[str]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "given": self.given,
            "when": self.when,
            "then": self.then,
        }


@dataclass
class Requirement:
    """Represents a requirement (### Requirement:) from a spec section."""
    title: str
    description: str
    section: str  # ADDED, MODIFIED, REMOVED, RENAMED
    scenarios: List[Scenario]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "section": self.section,
            "scenarios": [s.to_dict() for s in self.scenarios],
        }

    def get_params(self) -> List[str]:
        """Extract parameter names from scenario given/when steps."""
        params = set()
        for scenario in self.scenarios:
            for step in scenario.given + scenario.when:
                words = step.lower().split()
                for word in words:
                    if word.startswith("a ") or word.startswith("an "):
                        idx = words.index(word)
                        if idx + 1 < len(words):
                            params.add(words[idx + 1])
        return sorted(list(params))


@dataclass
class CapabilitySpec:
    """Represents a complete capability spec file."""
    name: str
    description: str
    requirements: Dict[str, Requirement]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "requirements": {
                k: v.to_dict() for k, v in self.requirements.items()
            },
        }

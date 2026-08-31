import re
from pathlib import Path
from typing import Dict, List
from src.openspec_core.models import Scenario, Requirement, CapabilitySpec


class SpecParser:
    """Parse OpenSpec .md files into structured Python objects."""

    def __init__(self, spec_dir: str = "openspec/specs"):
        self.spec_dir = Path(spec_dir)

    def parse(self, spec_file: Path) -> CapabilitySpec:
        """Parse a single spec.md file."""
        with open(spec_file, "r") as f:
            content = f.read()

        # Extract title from # heading
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Unknown"

        # Extract description (text between title and first ## section header)
        desc_match = re.search(
            r"^# .+\n\n(.+?)\n\n## (?:ADDED|MODIFIED|REMOVED|RENAMED)",
            content,
            re.MULTILINE | re.DOTALL
        )
        description = desc_match.group(1).strip() if desc_match else ""

        requirements = {}

        # Extract sections (## ADDED/MODIFIED/REMOVED/RENAMED Requirements)
        for section_match in re.finditer(
            r"## (ADDED|MODIFIED|REMOVED|RENAMED) Requirements", content
        ):
            section_type = section_match.group(1)
            section_start = section_match.start()
            
            # Find next section or end of file
            next_section = re.search(
                r"^## ", content[section_match.end():], re.MULTILINE
            )
            section_end = (
                section_match.end() + next_section.start()
                if next_section
                else len(content)
            )

            section_text = content[section_start:section_end]

            # Extract requirements (### Requirement:)
            for req_match in re.finditer(
                r"### Requirement: (.+)", section_text
            ):
                req_title = req_match.group(1).strip()
                req_start = req_match.end()
                
                # Find next requirement or end of section
                next_req = re.search(
                    r"^### Requirement:", section_text[req_start:], re.MULTILINE
                )
                req_end = (
                    req_start + next_req.start()
                    if next_req
                    else len(section_text)
                )
                
                req_text = section_text[req_match.start():req_end]
                
                # Get description (first line after title before scenarios)
                desc_lines = re.split(
                    r"\n#### Scenario:", req_text, maxsplit=1
                )[0]
                desc_lines = desc_lines.split("\n")[1:]
                req_desc = " ".join([l.strip() for l in desc_lines if l.strip()])

                # Extract scenarios (#### Scenario:)
                scenarios = []
                for scenario_match in re.finditer(
                    r"#### Scenario: (.+)", req_text
                ):
                    scenario_title = scenario_match.group(1).strip()
                    scenario_start = scenario_match.end()
                    
                    # Find next scenario or end
                    next_scenario = re.search(
                        r"^#### Scenario:", req_text[scenario_start:], re.MULTILINE
                    )
                    scenario_end = (
                        scenario_start + next_scenario.start()
                        if next_scenario
                        else len(req_text)
                    )
                    
                    scenario_text = req_text[scenario_start:scenario_end]

                    # Parse Given/When/Then
                    given = self._extract_steps(scenario_text, "Given")
                    when = self._extract_steps(scenario_text, "When")
                    then = self._extract_steps(scenario_text, "Then")

                    scenarios.append(
                        Scenario(
                            title=scenario_title,
                            given=given,
                            when=when,
                            then=then,
                        )
                    )

                req_key = req_title.lower().replace(" ", "_")[:50]  # Limit key length
                requirements[req_key] = Requirement(
                    title=req_title,
                    description=req_desc,
                    section=section_type,
                    scenarios=scenarios,
                )

        return CapabilitySpec(
            name=title,
            description=description,
            requirements=requirements,
        )

    def parse_all(self) -> Dict[str, CapabilitySpec]:
        """Parse all specs in the spec directory."""
        specs = {}
        for spec_file in self.spec_dir.glob("*/spec.md"):
            capability_name = spec_file.parent.name
            try:
                specs[capability_name] = self.parse(spec_file)
            except Exception as e:
                print(f"Error parsing {spec_file}: {e}")
        return specs

    @staticmethod
    def _extract_steps(text: str, step_type: str) -> List[str]:
        """Extract steps of a given type (Given, When, Then).
        
        Supports both formats:
        - "Given X, When Y, Then Z" (inline)
        - "Given: X\nWhen: Y\nThen: Z" (structured)
        """
        # Try structured format first (Given: / When: / Then:)
        pattern = rf"(?:^|\n){step_type}:?\s+(.+?)(?=\n(?:Given|When|Then):|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        if not match:
            # Try inline format: "Given X, when Y, then Z"
            # Extract the part between step_type and the next keyword
            pattern_inline = (
                rf"(?:^|,\s*){step_type}\s+([^,]+?)(?=,\s*(?:Given|When|Then)|$)"
            )
            match = re.search(pattern_inline, text, re.IGNORECASE)
            if not match:
                return []
            return [match.group(1).strip()]
        
        # Split by bullet points or line breaks
        steps_text = match.group(1).strip()
        steps = [s.strip() for s in re.split(r"[-•]\s+", steps_text) if s.strip()]
        return steps if steps else [steps_text]

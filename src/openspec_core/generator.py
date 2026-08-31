from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import re
from typing import Any

class CodeGenerator:
    def __init__(self, template_dir: str = "src/openspec_core/templates") -> None:
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape([]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["snake_case"] = self.snake_case
        self.env.filters["title_case"] = self.title_case

    def snake_case(self, s: str) -> str:
        s = s or ""
        s = re.sub(r"[^0-9a-zA-Z]+", "_", s)
        s = re.sub(r"_+", "_", s)
        return s.strip("_").lower()

    def title_case(self, s: str) -> str:
        return (s or "").title().replace(" ", "")

    def render_function(self, requirement: Any) -> str:
        tmpl = self.env.get_template("function_stub.j2")
        return tmpl.render(requirement=requirement)

    def render_test(self, scenario: Any) -> str:
        tmpl = self.env.get_template("test_stub.j2")
        return tmpl.render(scenario=scenario)

    def generate_functions(self, capability: Any, output_dir: str) -> None:
        """Generate Python function stubs for each requirement in a capability."""
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for req_key, req in capability.requirements.items():
            filename = out_dir / f"{self.snake_case(req.title)}.py"
            content = self.render_function(req)
            # Add imports
            header = "from typing import Any\n\n"
            filename.write_text(header + content)

    def generate_tests(self, capability: Any, tests_dir: str) -> None:
        """Generate pytest test files for scenarios in a capability."""
        out_dir = Path(tests_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for req_key, req in capability.requirements.items():
            for scenario in req.scenarios:
                test_name = f"test_{self.snake_case(req.title)}_{self.snake_case(scenario.title)}.py"
                filename = out_dir / test_name
                content = self.render_test(scenario)
                header = "import pytest\n\n"
                filename.write_text(header + content)

    def generate_config_class(self, sections: dict, output_file: str) -> None:
        """Generate a Pydantic AppConfig class from a sections dict and write to output_file."""
        tmpl = self.env.get_template("config_class.j2")
        content = tmpl.render(sections=sections)
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)

    def generate_from_specs(self, specs: dict, output_dir: str, tests_dir: str) -> None:
        """Full generation: for each capability generate functions and tests."""
        for name, capability in specs.items():
            cap_out = Path(output_dir) / name
            cap_tests = Path(tests_dir) / name
            self.generate_functions(capability, str(cap_out))
            self.generate_tests(capability, str(cap_tests))

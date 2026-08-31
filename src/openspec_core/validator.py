import inspect
import importlib.util
from pathlib import Path
from typing import List, Dict, Any

class ValidationResult:
    def __init__(self):
        self.signature_mismatches = []
        self.missing_docstrings = []
        self.missing_tests = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_mismatches": self.signature_mismatches,
            "missing_docstrings": self.missing_docstrings,
            "missing_tests": self.missing_tests,
        }


class Validator:
    def __init__(self, generated_dir: str, tests_dir: str, parsed_specs: Dict[str, Any]):
        self.generated_dir = Path(generated_dir)
        self.tests_dir = Path(tests_dir)
        self.parsed_specs = parsed_specs

    def _load_module_from_file(self, path: Path):
        spec = importlib.util.spec_from_file_location(path.stem, str(path))
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)  # type: ignore
            return module
        except Exception as e:
            print(f"Error importing {path}: {e}")
            return None

    def validate_signatures(self) -> List[str]:
        issues = []
        # For each generated file, compare with spec requirement params
        for cap_name, cap in self.parsed_specs.items():
            gen_dir = self.generated_dir / cap_name
            if not gen_dir.exists():
                issues.append(f"Missing generated directory for {cap_name}")
                continue
            for req_key, req in cap.requirements.items():
                func_name = req.title.lower().replace(" ", "_")
                file_path = gen_dir / f"{func_name}.py"
                if not file_path.exists():
                    issues.append(f"Missing generated file {file_path}")
                    continue
                module = self._load_module_from_file(file_path)
                if not module:
                    issues.append(f"Failed to import {file_path}")
                    continue
                # find function
                fn = getattr(module, func_name, None)
                if not fn:
                    issues.append(f"Function {func_name} not found in {file_path}")
                    continue
                sig = inspect.signature(fn)
                expected = req.get_params()
                actual = [p.name for p in sig.parameters.values()]
                if expected != actual:
                    issues.append(
                        f"Signature mismatch for {func_name}: expected {expected}, actual {actual}"
                    )
        return issues

    def check_docstrings(self) -> List[str]:
        issues = []
        for cap_name, cap in self.parsed_specs.items():
            gen_dir = self.generated_dir / cap_name
            for req_key, req in cap.requirements.items():
                func_name = req.title.lower().replace(" ", "_")
                file_path = gen_dir / f"{func_name}.py"
                if not file_path.exists():
                    issues.append(f"Missing generated file {file_path}")
                    continue
                module = self._load_module_from_file(file_path)
                if not module:
                    issues.append(f"Failed to import {file_path}")
                    continue
                fn = getattr(module, func_name, None)
                if not fn:
                    issues.append(f"Function {func_name} not found in {file_path}")
                    continue
                if not inspect.getdoc(fn):
                    issues.append(f"Missing docstring for {func_name}")
        return issues

    def check_test_coverage(self) -> List[str]:
        issues = []
        for cap_name, cap in self.parsed_specs.items():
            tests_cap_dir = self.tests_dir / cap_name
            if not tests_cap_dir.exists():
                issues.append(f"Missing tests for capability {cap_name}")
                continue
            # ensure each scenario has a test file
            for req_key, req in cap.requirements.items():
                for scenario in req.scenarios:
                    expected_file = tests_cap_dir / f"test_{req_key}_{scenario.title.lower().replace(' ', '_')}.py"
                    # Allow any test that contains req title and scenario title
                    found = False
                    if tests_cap_dir.exists():
                        for f in tests_cap_dir.glob("*.py"):
                            text = f.read_text()
                            if req.title.split()[0].lower() in text.lower() and scenario.title.split()[0].lower() in text.lower():
                                found = True
                                break
                    if not found:
                        issues.append(f"Missing test for scenario '{scenario.title}' in requirement '{req.title}'")
        return issues

    def generate_report(self) -> Dict[str, Any]:
        result = ValidationResult()
        result.signature_mismatches = self.validate_signatures()
        result.missing_docstrings = self.check_docstrings()
        result.missing_tests = self.check_test_coverage()
        return result.to_dict()

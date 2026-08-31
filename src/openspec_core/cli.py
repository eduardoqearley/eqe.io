"""CLI workflow: parse specs -> generate code -> validate -> report"""
from src.openspec_core.parser import SpecParser
from src.openspec_core.generator import CodeGenerator
from src.openspec_core.validator import Validator
from src.openspec_core.config import AppConfig
from pathlib import Path
import json


def run_workflow(config_path: str = "config.yaml"):
    cfg = AppConfig.load(config_path)

    parser = SpecParser(spec_dir=cfg.generator.template_dir.replace("templates", "../../openspec/changes/demo/specs"))
    specs = parser.parse_all()

    gen = CodeGenerator(template_dir=cfg.generator.template_dir)
    output_dir = cfg.generator.output_dir
    tests_dir = Path("tests_generated")
    gen.generate_from_specs(specs, output_dir, str(tests_dir))

    validator = Validator(generated_dir=output_dir, tests_dir=str(tests_dir), parsed_specs=specs)
    report = validator.generate_report()

    report_file = Path("openspec/changes/demo/report.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run_workflow()

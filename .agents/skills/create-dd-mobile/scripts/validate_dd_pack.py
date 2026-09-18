#!/usr/bin/env python3
"""Static validator for NanoBio DD modules, templates, and example packs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "README.md",
    "Overall.md",
    "List_Features.md",
    "Function_List.md",
    "Views.md",
    "Import_File.md",
    "diagrams/README.md",
    "assets/README.md",
    "history/CHANGELOG.md",
)
TEMPLATE_HISTORY = ("history/README.md", "history/CHANGELOG.md")
STATUS_VALUES = {
    "Lifecycle": {"Current", "Historical", "Generated", "Reference", "Source", "Binary"},
    "DD decision": {"Draft", "In Review", "Approved", "Deprecated"},
    "Implementation": {"Implemented", "Partial", "Placeholder", "Source-only", "Absent", "N/A"},
    "Verification": {"Static-verified", "Runtime-unverified", "Sandbox-unverified", "Historical"},
}
ID_PATTERN = re.compile(
    r"\b[A-Z][A-Z0-9_]*(?:-(?:F|FN|V|BR|API|ADR|TC)\d{2}|-E-[A-Za-z0-9_-]+)\b"
)
HEADING_ID_PATTERN = re.compile(
    r"^#{1,2}\s+.*?\b([A-Z][A-Z0-9_]*(?:-(?:F|FN|V|BR|API|ADR|TC)\d{2}|-E-[A-Za-z0-9_-]+))\b"
)
PLACEHOLDER_PATTERN = re.compile(r"\{\{|\[MODULE_CODE\]|\[MODULE NAME\]|\{\{[^}]+\}\}")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{24,}"),
)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


class Report:
    def __init__(self, label: str) -> None:
        self.label = label
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def ok(self) -> bool:
        return not self.failures

    def print(self) -> None:
        status = "PASS" if self.ok else "FAIL"
        print(f"[{status}] {self.label}")
        for message in self.failures:
            print(f"  FAIL: {message}")
        for message in self.warnings:
            print(f"  WARN: {message}")


def markdown_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.md")) if root.exists() else []


def validate_links(root: Path, report: Report) -> None:
    for path in markdown_files(root):
        content = path.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(content):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target):
                continue
            target_path = (path.parent / unquote(target)).resolve()
            if not target_path.exists():
                report.fail(f"broken link in {path.relative_to(root)}: {raw_target}")


def validate_status(root: Path, report: Report) -> None:
    readme = root / "README.md"
    if not readme.exists():
        return
    content = readme.read_text(encoding="utf-8")
    for field, allowed in STATUS_VALUES.items():
        match = re.search(rf"^\|\s*{re.escape(field)}\s*\|\s*([^|]+)\|", content, re.MULTILINE)
        if not match:
            report.warn(f"README.md has no explicit {field} status")
            continue
        raw = match.group(1).strip().strip("`")
        if field == "Verification":
            values = {part.strip().strip("`") for part in re.split(r"[;,]", raw)}
            if not any(value in allowed for value in values):
                report.fail(f"invalid {field} value: {raw}")
        elif not any(value in raw for value in allowed):
            report.fail(f"invalid {field} value: {raw}")


def validate_ids(root: Path, report: Report) -> None:
    definitions: dict[str, Path] = {}
    for path in markdown_files(root):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = HEADING_ID_PATTERN.match(line)
            if not match:
                continue
            identifier = match.group(1)
            if identifier in definitions:
                report.fail(
                    f"duplicate heading ID {identifier}: {definitions[identifier].relative_to(root)} and "
                    f"{path.relative_to(root)}:{line_number}"
                )
            else:
                definitions[identifier] = path
            if not ID_PATTERN.fullmatch(identifier):
                report.fail(f"invalid ID format {identifier} in {path.relative_to(root)}:{line_number}")


def validate_traceability(root: Path, report: Report) -> None:
    locations: dict[str, set[str]] = {}
    for path in markdown_files(root):
        if path.name == "README.md":
            continue
        for identifier in ID_PATTERN.findall(path.read_text(encoding="utf-8")):
            locations.setdefault(identifier, set()).add(path.name)

    required_locations = {
        "-F": (re.compile(r"-F(?!N)\d{2}$"), {"List_Features.md"}),
        "-FN": (re.compile(r"-FN\d{2}$"), {"Function_List.md"}),
        "-V": (re.compile(r"-V\d{2}$"), {"Views.md"}),
        "-BR": (re.compile(r"-BR\d{2}$"), {"Overall.md", "List_Features.md", "Function_List.md"}),
        "-API": (re.compile(r"-API\d{2}$"), {"Overall.md", "List_Features.md", "Function_List.md", "Import_File.md"}),
    }
    for _, (suffix_pattern, allowed_files) in required_locations.items():
        for candidate in sorted(name for name in locations if suffix_pattern.search(name)):
            if not locations[candidate].intersection(allowed_files) and not any(
                name.startswith("Implementation_Delta") for name in locations[candidate]
            ):
                report.fail(
                    f"traceability ID {candidate} is not documented in one of "
                    f"{sorted(allowed_files)}"
                )


def validate_sensitive_content(root: Path, report: Report) -> None:
    for path in markdown_files(root):
        content = path.read_text(encoding="utf-8")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                report.fail(f"possible secret/token in {path.relative_to(root)}")


def validate_module(root: Path, *, allow_placeholders: bool = False) -> Report:
    report = Report(str(root))
    for required in REQUIRED_FILES:
        if not (root / required).is_file():
            if allow_placeholders and required == "history/CHANGELOG.md" and any(
                (root / candidate).is_file() for candidate in TEMPLATE_HISTORY
            ):
                continue
            report.fail(f"missing required file: {required}")
    if not root.is_dir():
        report.fail("path is not a directory")
        report.print()
        return report
    if not allow_placeholders:
        for path in markdown_files(root):
            content = path.read_text(encoding="utf-8")
            if PLACEHOLDER_PATTERN.search(content):
                report.fail(f"template placeholder remains in {path.relative_to(root)}")
    validate_ids(root, report)
    if not allow_placeholders:
        validate_traceability(root, report)
    validate_status(root, report)
    validate_sensitive_content(root, report)
    validate_links(root, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--module", type=Path, help="Validate one DD module")
    group.add_argument("--examples", type=Path, help="Validate every immediate example directory")
    group.add_argument("--template", type=Path, help="Validate a template, allowing placeholders")
    args = parser.parse_args(argv)

    reports: list[Report] = []
    if args.module:
        reports.append(validate_module(args.module))
    elif args.template:
        reports.append(validate_module(args.template, allow_placeholders=True))
    else:
        example_dirs = sorted(path for path in args.examples.iterdir() if path.is_dir())
        if not example_dirs:
            print(f"[FAIL] {args.examples}: no example directories found")
            return 1
        reports.extend(validate_module(path) for path in example_dirs)

    for report in reports:
        report.print()
    return 0 if all(report.ok for report in reports) else 1


if __name__ == "__main__":
    sys.exit(main())

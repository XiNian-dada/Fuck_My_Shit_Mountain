#!/usr/bin/env python3
"""Lint Markdown, HTML and JSON audit reports using only the standard library."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from schema_validation import validate_schema

SKILL_DIR = Path(__file__).resolve().parents[1]
SEVERITIES = ("Critical", "High", "Medium", "Low", "Info")
CONFIDENCES = ("High", "Medium", "Low")
STATUSES = ("Confirmed", "Suspected")
# Prompt filenames are the authoritative mode registry.
FULL_SECTION_IDS = tuple(sorted(
    path.name.removesuffix("-audit.md") for path in (SKILL_DIR / "prompts").glob("*-audit.md")
    if path.name not in {"full-audit.md", "incremental-audit.md"}
))
SECTIONS = {
    "executive-summary": ("Executive Summary", "总体评估", "执行摘要"),
    "score-dashboard": ("Score Dashboard", "评分面板"),
    "project-map": ("Project Map", "项目地图"),
    "coverage": ("Coverage Matrix", "覆盖矩阵"),
    "statistics": ("Finding Statistics", "发现统计"),
    "top-risks": ("Top Risks", "最高风险", "主要风险"),
    "findings": ("Detailed Findings", "详细发现"),
    "fix-order": ("Recommended Fix Order", "建议修复顺序", "修复顺序"),
    "quick-wins": ("Quick Wins", "速赢项", "快速改进"),
}
FIELDS = {
    "severity": ("Severity", "严重程度"),
    "confidence": ("Confidence", "置信度"),
    "category": ("Category", "类别"),
    "status": ("Status", "状态"),
    "affectedArea": ("Affected area", "受影响区域"),
    "evidence": ("Evidence", "证据"),
    "problem": ("Problem", "问题"),
    "userVisibleImpact": ("Why it matters", "User-visible impact", "影响", "影响说明"),
    "failureScenario": ("Realistic failure scenario", "Failure scenario", "实际故障场景", "故障场景"),
    "minimalFix": ("Minimal fix", "最小修复"),
    "regressionTestSuggestion": ("Regression test suggestion", "回归验证建议", "回归测试建议"),
    "estimatedEffort": ("Estimated effort", "预计工作量"),
}
PLACEHOLDER = re.compile(r"\[\[[^\]\n]+\]\]|<(?:project name|date|short title|N|dimension|selected modes?)>", re.I)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----"),
    re.compile(r'''(?i)["']?\b(api[_-]?key|access[_-]?token|auth[_-]?token|secret|password|passwd)\b["']?\s*[:=]\s*["']?(?!<redacted>|redacted\b)[A-Za-z0-9_./+=:-]{16,}'''),
)


def lint_secrets(text: str, issues: list[str]) -> None:
    for pattern in SECRET_PATTERNS:
        match = pattern.search(html.unescape(text))
        if match:
            # Never include matched content, even in a failed-lint diagnostic.
            line = text.count("\n", 0, min(match.start(), len(text))) + 1
            issues.append(f"Possible unredacted secret near line {line}; value withheld")


def expand_modes(modes: str | None, issues: list[str]) -> tuple[str, ...]:
    selected = list(dict.fromkeys(re.split(r"[,\s]+", (modes or "").strip().lower())))
    selected = [mode for mode in selected if mode]
    for mode in selected:
        if mode not in {*FULL_SECTION_IDS, "full", "incremental"}:
            issues.append("Unknown audit mode; use a prompt filename without '-audit.md'")
    focused = tuple(mode for mode in selected if mode in FULL_SECTION_IDS)
    return FULL_SECTION_IDS if "full" in selected or ("incremental" in selected and not focused) else focused


def check_findings(findings: list[dict], issues: list[str]) -> None:
    ids = [item.get("id") for item in findings if item.get("id")]
    if len(ids) != len(set(ids)):
        issues.append("Duplicate finding ID")
    for index, finding in enumerate(findings, 1):
        for field in FIELDS:
            if not finding.get(field):
                issues.append(f"Finding #{index} missing or empty field: {field}")
        for field, allowed in (("severity", SEVERITIES), ("confidence", CONFIDENCES), ("status", STATUSES)):
            if finding.get(field) not in allowed:
                issues.append(f"Finding #{index} invalid {field}")


def check_stats(findings: list[dict], stats: dict[str, tuple[int, int, int]], issues: list[str]) -> None:
    for severity in (*SEVERITIES, "Total"):
        rows = findings if severity == "Total" else [item for item in findings if item.get("severity") == severity]
        expected = (len(rows), sum(item.get("status") == "Confirmed" for item in rows), sum(item.get("status") == "Suspected" for item in rows))
        if stats.get(severity) != expected:
            issues.append(f"Finding statistics missing or inconsistent: {severity}")


def markdown_findings(text: str) -> list[dict]:
    starts = list(re.finditer(r"(?m)^<!--\s*finding:([\w-]+)\s*-->\s*$", text))
    if not starts:
        starts = list(re.finditer(r"(?mi)^###\s+(?:Finding|发现|问题)[:：]", text))
    findings = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        chunk = re.split(r"(?m)^##\s|^<!--\s*section:", text[start.end():end], maxsplit=1)[0]
        finding = {"id": start.group(1)} if start.lastindex else {}
        current = None
        for line in chunk.splitlines():
            if line.startswith("- "):
                marker = re.search(r"<!--\s*field:(\w+)\s*-->", line)
                label, _, value = re.sub(r"<!--.*?-->", "", line[2:]).replace("**", "").replace("：", ":").partition(":")
                current = marker.group(1) if marker else next((key for key, labels in FIELDS.items() if label.strip().lower() in [item.lower() for item in labels]), None)
                if current:
                    finding[current] = value.strip()
            elif current and line.strip():
                finding[current] += "\n" + line.strip()
        findings.append(finding)
    return findings


def lint_markdown(text: str, modes: str | None, issues: list[str]) -> None:
    # Example code blocks are evidence, not report structure or finding records.
    text = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text)
    markers = set(re.findall(r"<!--\s*section:([\w-]+)\s*-->", text))
    headings = re.findall(r"(?m)^#{2,6}\s+(.+)$", text)
    for section, labels in SECTIONS.items():
        if section not in markers and not any(any(label.lower() in heading.lower() for label in labels) for heading in headings):
            issues.append(f"Missing report section: {section}")
    for mode in expand_modes(modes, issues):
        label = mode.replace("-", " ")
        if mode not in markers and not any(label.lower() in heading.lower() for heading in headings):
            issues.append(f"Missing selected dimension section: {mode}")
    findings = markdown_findings(text)
    check_findings(findings, issues)
    stats = {}
    for row in re.finditer(r"(?mi)^\|\s*\**(Critical|High|Medium|Low|Info|Total|总计)\**\s*\|\s*\**(\d+)\**\s*\|\s*\**(\d+)\**\s*\|\s*\**(\d+)\**\s*\|", text):
        severity = "Total" if row.group(1) == "总计" else row.group(1).capitalize()
        if severity in stats:
            issues.append(f"Duplicate statistics row: {severity}")
        stats[severity] = tuple(int(row.group(i)) for i in (2, 3, 4))
    check_stats(findings, stats, issues)


class ReportHTML(HTMLParser):
    """Read actual elements rather than accepting IDs hidden in comments."""
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.findings, self.stack, self.issues = [], [], [], [], []
        self.stats = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.links.append(attrs["href"][1:])
        finding = self.stack[-1]["finding"] if self.stack else None
        if "data-finding" in attrs:
            finding = {"id": attrs["data-finding"]}
            self.findings.append(finding)
        if "data-stat" in attrs:
            severity = attrs["data-stat"]
            if severity in self.stats:
                self.issues.append("Duplicate HTML statistics row")
            try:
                self.stats[severity] = tuple(int(attrs[key]) for key in ("data-count", "data-confirmed", "data-suspected"))
            except (ValueError, KeyError, TypeError):
                self.issues.append("Invalid HTML finding statistics")
        if tag not in self.VOID_TAGS:
            self.stack.append({"tag": tag, "field": attrs.get("data-field"), "finding": finding, "text": []})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)

    def handle_data(self, data):
        for frame in self.stack:
            frame["text"].append(data)

    def handle_endtag(self, tag):
        if tag in self.VOID_TAGS:
            return
        if not self.stack or self.stack[-1]["tag"] != tag:
            self.issues.append("Unbalanced HTML tags")
            return
        frame = self.stack.pop()
        if frame["field"] and frame["finding"] is not None:
            field = frame["field"]
            if field in frame["finding"]:
                self.issues.append("Duplicate finding field in HTML")
            frame["finding"][field] = "".join(frame["text"]).strip()


def lint_html(text: str, modes: str | None, issues: list[str]) -> None:
    report = ReportHTML()
    report.feed(text)
    report.close()
    issues.extend(report.issues)
    if report.stack:
        issues.append("Unclosed HTML tags")
    if len(report.ids) != len(set(report.ids)):
        issues.append("Duplicate HTML element ID")
    for section in (*SECTIONS, *expand_modes(modes, issues)):
        if section not in report.ids:
            issues.append(f"Missing HTML section id: {section}")
    if any(link not in report.ids for link in report.links):
        issues.append("Broken internal HTML navigation link")
    check_findings(report.findings, issues)
    check_stats(report.findings, report.stats, issues)


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON property")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("Non-finite JSON number")


def grade(score: float) -> str:
    return next(label for floor, label in ((9, "S"), (7, "A"), (5, "B"), (3, "C"), (1, "D"), (0, "F")) if score >= floor)


def lint_json(text: str, modes: str | None, issues: list[str]) -> None:
    try:
        report = json.loads(text, object_pairs_hook=reject_duplicates, parse_constant=reject_constant)
    except (json.JSONDecodeError, ValueError):
        issues.append("Invalid JSON, duplicate property, or non-finite number")
        return
    lint_secrets(json.dumps(report, ensure_ascii=False), issues)
    schema = json.loads((SKILL_DIR / "templates/audit-report.json").read_text(encoding="utf-8"))
    schema["properties"]["metadata"]["properties"]["auditModes"]["items"]["enum"] = ["full", "incremental", *FULL_SECTION_IDS]
    schema_issues = validate_schema(report, schema)
    issues.extend(schema_issues)
    if schema_issues:
        return
    selected = expand_modes(",".join(report["metadata"]["auditModes"]), issues)
    if modes and set(selected) != set(expand_modes(modes, issues)):
        issues.append("Requested modes differ from JSON metadata modes")
    if "incremental" in report["metadata"]["auditModes"] and not report["metadata"].get("scope"):
        issues.append("Incremental JSON report requires its resolved Git scope")
    covered = [row["dimension"] for row in report["coverageMatrix"]]
    if len(covered) != len(set(covered)):
        issues.append("Duplicate coverage dimension")
    if set(report["dimensionSections"]) - set(FULL_SECTION_IDS):
        issues.append("Unknown dimension analysis key; use canonical mode IDs")
    for mode in selected:
        if mode not in covered or mode not in report["dimensionSections"]:
            issues.append(f"Missing coverage or analysis for selected dimension: {mode}")
    findings = report["detailedFindings"]
    check_findings(findings, issues)
    stats = {row["severity"]: tuple(row[key] for key in ("count", "confirmed", "suspected")) for row in report["findingStatistics"]["bySeverity"]}
    if len(stats) != len(report["findingStatistics"]["bySeverity"]):
        issues.append("Duplicate JSON statistics row")
    stats["Total"] = tuple(report["findingStatistics"]["total"][key] for key in ("count", "confirmed", "suspected"))
    check_stats(findings, stats, issues)
    ids = {item["id"] for item in findings}
    for item in [*report["topRisks"], *report["fixOrder"], *report["quickWins"]]:
        if item.get("findingId") not in ids:
            issues.append("Report reference points to a missing finding")
    dimensions = report["scoreDashboard"]["dimensions"]
    if len({row["name"] for row in dimensions}) != len(dimensions):
        issues.append("Duplicate score dimension")
    assessed = {}
    for row in dimensions:
        score = row["score"]
        if row["coverageConfidence"] == "Not assessed":
            if score is not None or row["grade"] is not None:
                issues.append("Not assessed dimensions must have null score and grade")
        elif score is None or row["grade"] != grade(score):
            issues.append("Assessed dimension has missing score or inconsistent grade")
        else:
            assessed[row["name"]] = score
    weights = report["scoreDashboard"].get("intelligentWeights", {}).get("weights")
    if weights is not None:
        if set(weights) != set(assessed) or sum(weights.values()) <= 0:
            issues.append("Weights must cover exactly the assessed score dimensions with a positive total")
            return
        expected = round(sum(assessed[name] * weights[name] for name in assessed) / sum(weights.values()), 1)
    else:
        expected = round(sum(assessed.values()) / len(assessed), 1) if assessed else None
    overall = report["scoreDashboard"]["overall"]
    if overall["score"] != expected or overall["grade"] != (grade(expected) if expected is not None else None):
        issues.append("Overall score or grade is inconsistent with assessed dimensions")


def lint_report(path: Path, modes: str | None = None) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8")
    lint_secrets(text, issues)
    if PLACEHOLDER.search(text):
        issues.append("Unreplaced template placeholder; content withheld")
    suffix = path.suffix.lower()
    if suffix == ".json":
        lint_json(text, modes, issues)
    elif suffix in {".html", ".htm"}:
        lint_html(text, modes, issues)
    elif suffix in {".md", ".markdown"}:
        lint_markdown(text, modes, issues)
    else:
        issues.append("Unsupported report format; expected Markdown, HTML, or JSON")
    return issues


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modes", help="Comma-separated audit modes; incremental may be combined with focused modes")
    parser.add_argument("reports", nargs="+", type=Path, help="Generated .md, .html or .json reports")
    args = parser.parse_args(argv)
    exit_code = 0
    for report in args.reports:
        try:
            issues = lint_report(report, args.modes)
        except (OSError, UnicodeError):
            print(f"{report}: unreadable report or skill resource", file=sys.stderr)
            exit_code = max(exit_code, 2)
            continue
        if issues:
            exit_code = max(exit_code, 1)
            print(f"{report}: FAIL")
            for issue in dict.fromkeys(issues):
                print(f"  - {issue}")
        else:
            print(f"{report}: OK")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

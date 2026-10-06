"""Validate the keywords used by the bundled report schema, without dependencies.

This is not a general JSON Schema implementation. Unsupported assertion
keywords fail explicitly so schema changes cannot silently weaken lint.
"""
from __future__ import annotations

import math
import re
from datetime import date

ANNOTATIONS = {"$schema", "title", "description", "$comment", "default"}
ASSERTIONS = {
    "type", "enum", "required", "properties", "additionalProperties", "items",
    "minItems", "maxItems", "uniqueItems", "minimum", "maximum", "minLength", "format",
}


def validate_schema(value, schema: dict, path: str = "$", issues: list[str] | None = None) -> list[str]:
    if issues is None:
        issues = []
    if set(schema) - ANNOTATIONS - ASSERTIONS:
        issues.append(f"{path}: unsupported schema constraint; update the validator")
        return issues
    types = {
        "object": isinstance(value, dict), "array": isinstance(value, list),
        "string": isinstance(value, str), "null": value is None,
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }
    expected = schema.get("type")
    if expected and not any(types.get(kind, False) for kind in ([expected] if isinstance(expected, str) else expected)):
        issues.append(f"{path}: wrong value type")
        return issues
    if "enum" in schema and value not in schema["enum"]:
        issues.append(f"{path}: value is outside the allowed enum")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                issues.append(f"{path}.{key}: required field missing")
        properties = schema.get("properties", {})
        for key, child in value.items():
            if key in properties:
                validate_schema(child, properties[key], f"{path}.{key}", issues)
            else:
                additional = schema.get("additionalProperties", True)
                if additional is False:
                    issues.append(f"{path}: unexpected property")
                elif isinstance(additional, dict):
                    validate_schema(child, additional, f"{path}.*", issues)
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", math.inf):
            issues.append(f"{path}: invalid array length")
        if schema.get("uniqueItems") and any(item in value[:index] for index, item in enumerate(value)):
            issues.append(f"{path}: duplicate array item")
        for index, child in enumerate(value):
            if "items" in schema:
                validate_schema(child, schema["items"], f"{path}[{index}]", issues)
    elif isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            issues.append(f"{path}: empty or too-short text")
        if schema.get("format") == "date":
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError
                date.fromisoformat(value)
            except ValueError:
                issues.append(f"{path}: invalid ISO date")
        elif "format" in schema:
            issues.append(f"{path}: unsupported schema format")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if (isinstance(value, float) and not math.isfinite(value)) or not schema.get("minimum", -math.inf) <= value <= schema.get("maximum", math.inf):
            issues.append(f"{path}: number outside the allowed range")
    return issues

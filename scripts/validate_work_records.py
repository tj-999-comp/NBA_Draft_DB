#!/usr/bin/env python3
"""Validate the source-side work-record contract for NBA_Draft_DB.

The validator intentionally uses only the Python standard library.  Metadata is
the small, fixed YAML subset defined by the public work-record contract, so a
strict parser is preferable to making PyYAML a runtime dependency.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


PROJECT_ID = "NBA_Draft_DB"
BASE_RE = re.compile(r"^work_record_([0-9]{3})$")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^  -(?:\s+(.*))?$")
EXPECTED_KEYS = {
    "schema_version",
    "title",
    "date",
    "project_id",
    "tags",
    "publish",
}


class MetadataError(ValueError):
    """Raised when a metadata file is outside the fixed YAML subset."""


def _parse_scalar(value: str, *, field: str) -> Any:
    """Parse one scalar without accepting YAML features outside the contract."""

    if value == "":
        raise MetadataError(f"{field} must have a value")
    if value.startswith('"'):
        if not value.endswith('"'):
            raise MetadataError(f"{field} has an invalid quoted value")
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise MetadataError(f"{field} has an invalid quoted value") from exc
        if not isinstance(parsed, str):
            raise MetadataError(f"{field} must be a string")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'"):
            raise MetadataError(f"{field} has an invalid quoted value")
        return value[1:-1].replace("''", "'")
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"[0-9]+", value):
        return int(value)
    return value


def parse_metadata(path: Path) -> dict[str, Any]:
    """Parse and structurally validate one work-record metadata file."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise MetadataError("file is not valid UTF-8 or cannot be read") from exc

    if "\t" in text:
        raise MetadataError("tabs are not allowed")

    values: dict[str, Any] = {}
    tags: list[str] | None = None
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_match = LIST_ITEM_RE.fullmatch(line)
        if list_match:
            if tags is None:
                raise MetadataError("list item is only allowed under tags")
            item = list_match.group(1)
            if item is None:
                raise MetadataError("tags must contain strings")
            parsed_item = _parse_scalar(item, field="tags")
            if not isinstance(parsed_item, str) or not parsed_item:
                raise MetadataError("tags must contain non-empty strings")
            tags.append(parsed_item)
            continue
        if line[:1].isspace():
            raise MetadataError("unexpected indentation")
        key_match = TOP_LEVEL_KEY_RE.fullmatch(line)
        if not key_match:
            raise MetadataError("invalid mapping entry")
        key, raw_value = key_match.groups()
        if key in values or (key == "tags" and tags is not None):
            raise MetadataError("duplicate metadata key")
        if key == "tags":
            if raw_value not in ("", "[]"):
                raise MetadataError("tags must be a block list or []")
            tags = []
            values[key] = tags
            continue
        values[key] = _parse_scalar(raw_value, field=key)

    if set(values) != EXPECTED_KEYS:
        missing = EXPECTED_KEYS - set(values)
        unknown = set(values) - EXPECTED_KEYS
        details = []
        if missing:
            details.append("missing required metadata key")
        if unknown:
            details.append("unknown metadata key")
        raise MetadataError("; ".join(details))

    if values["schema_version"] != 1 or isinstance(values["schema_version"], bool):
        raise MetadataError("schema_version must be 1")
    if not isinstance(values["title"], str) or not values["title"].strip():
        raise MetadataError("title must be a non-empty string")
    if not isinstance(values["date"], str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", values["date"]
    ):
        raise MetadataError("date must use YYYY-MM-DD")
    try:
        dt.date.fromisoformat(values["date"])
    except ValueError as exc:
        raise MetadataError("date must be a real calendar date") from exc
    if values["project_id"] != PROJECT_ID:
        raise MetadataError("project_id does not match the repository contract")
    if not isinstance(values["tags"], list) or any(
        not isinstance(tag, str) for tag in values["tags"]
    ):
        raise MetadataError("tags must be an array of strings")
    if not isinstance(values["publish"], bool):
        raise MetadataError("publish must be true or false")
    return values


def _validate_record_files(directory: Path, suffix: str, errors: list[str]) -> set[str]:
    basenames: set[str] = set()
    if not directory.is_dir() or directory.is_symlink():
        errors.append(f"{directory}: required directory is missing")
        return basenames
    casefolded: set[str] = set()
    try:
        entries = sorted(directory.iterdir(), key=lambda item: item.name)
    except OSError:
        errors.append(f"{directory}: directory cannot be read")
        return basenames
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            errors.append(f"{entry}: only regular record files are allowed")
            continue
        if not entry.name.endswith(suffix):
            errors.append(f"{entry}: filename does not use the required extension")
            continue
        base = entry.name[: -len(suffix)]
        match = BASE_RE.fullmatch(base)
        if not match or not 1 <= int(match.group(1)) <= 999:
            errors.append(f"{entry}: basename must match work_record_001 through work_record_999")
            continue
        folded = base.casefold()
        if folded in casefolded:
            errors.append(f"{entry}: duplicate record basename")
            continue
        casefolded.add(folded)
        basenames.add(base)
    return basenames


def validate(
    root: Path,
    *,
    target_basename: str | None = None,
    require_publish: bool = False,
) -> list[str]:
    """Return all contract violations found below ``root``."""

    errors: list[str] = []
    if not root.is_dir() or root.is_symlink():
        return [f"{root}: work-records directory is missing"]

    expected_dirs = {"md", "metadata"}
    for entry in sorted(root.iterdir(), key=lambda item: item.name):
        if entry.name not in expected_dirs:
            errors.append(f"{entry}: unexpected file or directory")

    md_dir = root / "md"
    metadata_dir = root / "metadata"
    markdown_basenames = _validate_record_files(md_dir, ".md", errors)
    metadata_basenames = _validate_record_files(metadata_dir, ".yml", errors)
    if markdown_basenames != metadata_basenames:
        errors.append("Markdown and metadata basenames must match one-to-one")

    metadata_by_base: dict[str, dict[str, Any]] = {}
    for base in sorted(metadata_basenames):
        path = metadata_dir / f"{base}.yml"
        try:
            metadata_by_base[base] = parse_metadata(path)
        except MetadataError as exc:
            errors.append(f"{path}: invalid metadata ({exc})")

    if target_basename is not None:
        if not BASE_RE.fullmatch(target_basename) or not 1 <= int(target_basename[-3:]) <= 999:
            errors.append("target_basename must match work_record_001 through work_record_999")
        elif target_basename not in markdown_basenames or target_basename not in metadata_basenames:
            errors.append("target_basename must have both Markdown and metadata files")
        else:
            metadata = metadata_by_base.get(target_basename)
            if metadata is not None and require_publish and metadata.get("publish") is not True:
                errors.append("target metadata must have publish: true")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("work-records"))
    parser.add_argument("--target-basename")
    parser.add_argument("--require-publish", action="store_true")
    args = parser.parse_args(argv)
    errors = validate(
        args.root,
        target_basename=args.target_basename,
        require_publish=args.require_publish,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated work-records contract: {args.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

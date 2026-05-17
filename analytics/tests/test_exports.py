from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from analytics.src.clean import load_raw_tables, validate_relationships
from analytics.src.config import ANALYTICS_OUTPUT_DIR, REQUIRED_EXPORTS, REQUIRED_TABLES, WEB_DATA_DIR
from analytics.src.export_dashboard_data import build_exports


def test_loads_all_required_raw_tables():
    tables = load_raw_tables()
    assert sorted(tables) == sorted(REQUIRED_TABLES)
    assert all(len(table) > 0 for table in tables.values())


def test_raw_table_relationships_are_valid():
    validate_relationships(load_raw_tables())


def test_builds_all_required_exports():
    exports = build_exports()
    assert sorted(exports) == sorted(REQUIRED_EXPORTS)
    for name, payload in exports.items():
        assert payload["generated_at"]
        assert payload["source"]
        assert payload.get("summary") is not None, name


def test_exported_json_files_exist_and_have_content():
    for output_dir in [ANALYTICS_OUTPUT_DIR, WEB_DATA_DIR]:
        for name in REQUIRED_EXPORTS:
            path = output_dir / name
            assert path.exists(), path
            payload = json.loads(path.read_text())
            assert payload["generated_at"]
            assert payload["source"]
            assert payload.get("summary") is not None

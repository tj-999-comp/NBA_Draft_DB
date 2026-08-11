#!/usr/bin/env python3
"""Create the canonical SQLite database, optionally loading sample data."""

from pathlib import Path
import argparse
import sqlite3


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path, help="SQLite database path")
    parser.add_argument("--sample", action="store_true", help="load the sample dataset")
    args = parser.parse_args()

    args.database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(args.database) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript((ROOT / "db/schema.sql").read_text())
        if args.sample:
            connection.executescript((ROOT / "db/sample_data.sql").read_text())


if __name__ == "__main__":
    main()

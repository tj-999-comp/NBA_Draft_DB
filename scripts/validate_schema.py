#!/usr/bin/env python3
"""Run the minimum schema/data checks required by AGENTS.md."""

from pathlib import Path
import argparse
import sqlite3


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    args = parser.parse_args()

    with sqlite3.connect(args.database) as db:
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        checks = {
            "player_id_unique": db.execute("SELECT COUNT(*) = COUNT(DISTINCT player_id) FROM players").fetchone()[0],
            "draft_players_exist": db.execute("SELECT COUNT(*) = 0 FROM draft_picks d LEFT JOIN players p USING (player_id) WHERE p.player_id IS NULL").fetchone()[0],
            "season_players_exist": db.execute("SELECT COUNT(*) = 0 FROM player_seasons s LEFT JOIN players p USING (player_id) WHERE p.player_id IS NULL").fetchone()[0],
            "no_negative_games": db.execute("SELECT COUNT(*) = 0 FROM player_seasons WHERE games_played < 0").fetchone()[0],
            "undrafted_fields_null": db.execute("SELECT COUNT(*) = 0 FROM draft_picks WHERE draft_status = 'undrafted' AND (draft_year IS NOT NULL OR draft_round IS NOT NULL OR overall_pick IS NOT NULL)").fetchone()[0],
            "appeared_implies_selected": db.execute("SELECT COUNT(*) = 0 FROM player_honors WHERE appeared = 1 AND selected = 0").fetchone()[0],
        }
        failed = [name for name, passed in checks.items() if not passed]
        print({"checks": checks, "status": "ok" if not failed else "failed"})
        if failed:
            raise SystemExit(f"failed checks: {', '.join(failed)}")


if __name__ == "__main__":
    main()

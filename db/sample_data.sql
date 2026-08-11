PRAGMA foreign_keys = ON;

BEGIN;

INSERT INTO players (player_id, display_name, birth_date, country, position, source_name, source_url, retrieved_at) VALUES
    ('p_001', 'Sample One', '1990-01-01', 'USA', 'G', 'sample', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('p_002', 'Sample Two', '1992-02-02', 'Canada', 'F', 'sample', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('p_003', 'Sample Three', '1995-03-03', 'France', 'C', 'sample', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('p_004', 'Sample Four', '1998-04-04', 'USA', 'G', 'sample', 'https://example.com/sample/players', '2026-08-11T00:00:00Z');

INSERT INTO player_external_ids (source_name, external_player_id, player_id, source_url, retrieved_at) VALUES
    ('sample', 'ext-001', 'p_001', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('sample', 'ext-002', 'p_002', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('sample', 'ext-003', 'p_003', 'https://example.com/sample/players', '2026-08-11T00:00:00Z'),
    ('sample', 'ext-004', 'p_004', 'https://example.com/sample/players', '2026-08-11T00:00:00Z');

INSERT INTO draft_picks (player_id, draft_year, draft_round, overall_pick, draft_team, draft_status, source_name, source_url, retrieved_at) VALUES
    ('p_001', 2010, 1, 5, 'Sample Hawks', 'drafted', 'sample', 'https://example.com/sample/draft', '2026-08-11T00:00:00Z'),
    ('p_002', 2012, 2, 35, 'Sample Bulls', 'drafted', 'sample', 'https://example.com/sample/draft', '2026-08-11T00:00:00Z'),
    ('p_003', 2015, 1, 10, 'Sample Lakers', 'drafted', 'sample', 'https://example.com/sample/draft', '2026-08-11T00:00:00Z'),
    ('p_004', NULL, NULL, NULL, NULL, 'undrafted', 'sample', 'https://example.com/sample/draft', '2026-08-11T00:00:00Z');

INSERT INTO player_seasons (player_id, season, team, games_played, starts, minutes, points, rebounds, assists, source_name, source_url, retrieved_at) VALUES
    ('p_001', '2010-11', 'Sample Hawks', 70, 20, 1400, 600, 200, 180, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z'),
    ('p_001', '2011-12', 'Sample Hawks', 66, 30, 1500, 700, 220, 200, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z'),
    ('p_001', '2013-14', 'Sample Bulls', 50, 10, 900, 400, 160, 100, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z'),
    ('p_002', '2012-13', 'Sample Bulls', 82, 60, 2200, 1000, 500, 250, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z'),
    ('p_003', '2015-16', 'Sample Lakers', 10, 0, 100, 30, 20, 5, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z'),
    ('p_004', '2020-21', 'Sample Nets', 25, 2, 400, 180, 80, 70, 'sample', 'https://example.com/sample/seasons', '2026-08-11T00:00:00Z');

INSERT INTO player_honors (player_id, season, honor_type, selected, appeared, source_name, source_url, retrieved_at) VALUES
    ('p_001', '2011-12', 'all_star', 1, 1, 'sample', 'https://example.com/sample/honors', '2026-08-11T00:00:00Z'),
    ('p_003', '2015-16', 'all_star', 1, 0, 'sample', 'https://example.com/sample/honors', '2026-08-11T00:00:00Z');

COMMIT;

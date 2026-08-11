PRAGMA foreign_keys = ON;

-- SQLite is the canonical source of truth for the MVP. Generated CSV/JSON
-- files must be derived from this database and must not be edited directly.

CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY CHECK (length(trim(player_id)) > 0),
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) > 0),
    birth_date TEXT,
    country TEXT,
    position TEXT,
    source_name TEXT NOT NULL CHECK (length(trim(source_name)) > 0),
    source_url TEXT NOT NULL CHECK (source_url LIKE 'http://%' OR source_url LIKE 'https://%'),
    retrieved_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS player_external_ids (
    source_name TEXT NOT NULL CHECK (length(trim(source_name)) > 0),
    external_player_id TEXT NOT NULL CHECK (length(trim(external_player_id)) > 0),
    player_id TEXT NOT NULL,
    source_url TEXT NOT NULL CHECK (source_url LIKE 'http://%' OR source_url LIKE 'https://%'),
    retrieved_at TEXT NOT NULL,
    PRIMARY KEY (source_name, external_player_id),
    UNIQUE (source_name, player_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS draft_picks (
    player_id TEXT PRIMARY KEY,
    draft_year INTEGER,
    draft_round INTEGER,
    overall_pick INTEGER,
    draft_team TEXT,
    draft_status TEXT NOT NULL CHECK (draft_status IN ('drafted', 'undrafted')),
    source_name TEXT NOT NULL CHECK (length(trim(source_name)) > 0),
    source_url TEXT NOT NULL CHECK (source_url LIKE 'http://%' OR source_url LIKE 'https://%'),
    retrieved_at TEXT NOT NULL,
    CHECK (
        (draft_status = 'undrafted' AND draft_year IS NULL AND draft_round IS NULL AND overall_pick IS NULL AND draft_team IS NULL)
        OR
        (draft_status = 'drafted' AND draft_year BETWEEN 1946 AND 2100 AND draft_round IN (1, 2) AND overall_pick >= 1 AND draft_team IS NOT NULL)
    ),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS player_seasons (
    player_id TEXT NOT NULL,
    season TEXT NOT NULL CHECK (season GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'),
    team TEXT NOT NULL CHECK (length(trim(team)) > 0),
    games_played INTEGER NOT NULL CHECK (games_played >= 0),
    starts INTEGER NOT NULL DEFAULT 0 CHECK (starts >= 0 AND starts <= games_played),
    minutes REAL CHECK (minutes IS NULL OR minutes >= 0),
    points REAL CHECK (points IS NULL OR points >= 0),
    rebounds REAL CHECK (rebounds IS NULL OR rebounds >= 0),
    assists REAL CHECK (assists IS NULL OR assists >= 0),
    source_name TEXT NOT NULL CHECK (length(trim(source_name)) > 0),
    source_url TEXT NOT NULL CHECK (source_url LIKE 'http://%' OR source_url LIKE 'https://%'),
    retrieved_at TEXT NOT NULL,
    PRIMARY KEY (player_id, season, team),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS player_honors (
    player_id TEXT NOT NULL,
    season TEXT NOT NULL CHECK (season GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'),
    honor_type TEXT NOT NULL CHECK (length(trim(honor_type)) > 0),
    selected INTEGER NOT NULL CHECK (selected IN (0, 1)),
    appeared INTEGER NOT NULL CHECK (appeared IN (0, 1)),
    source_name TEXT NOT NULL CHECK (length(trim(source_name)) > 0),
    source_url TEXT NOT NULL CHECK (source_url LIKE 'http://%' OR source_url LIKE 'https://%'),
    retrieved_at TEXT NOT NULL,
    PRIMARY KEY (player_id, season, honor_type),
    CHECK (appeared <= selected),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_player_seasons_season ON player_seasons(season);
CREATE INDEX IF NOT EXISTS idx_draft_picks_status_year ON draft_picks(draft_status, draft_year);
CREATE INDEX IF NOT EXISTS idx_player_honors_type ON player_honors(honor_type, selected);

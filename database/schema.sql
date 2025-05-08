CREATE TABLE IF NOT EXISTS team_aliases (
alias TEXT PRIMARY KEY,
team_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
team_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
shortname TEXT DEFAULT NULL,
tz TEXT default "America/Toronto",
created_by TEXT default NULL,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
lastmodified_by TEXT default NULL,
lastmodified_at timestamp default NULL
);

CREATE TABLE IF NOT EXISTS competitions (
competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT default NULL,
shortname TEXT NOT NULL,
logo_url TEXT default NULL,
color TEXT default NULL,
competition_type INTEGER default 0,
is_monitored BOOLEAN default FALSE,
is_international BOOLEAN default FALSE,
optout_role_id TEXT default NULL,
category_id TEXT default NULL,
hours_before_kickoff default NULL,
hours_after_kickoff default NULL,
created_by TEXT default NULL,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
lastmodified_by TEXT default NULL,
lastmodified_at timestamp default NULL
);

CREATE TABLE IF NOT EXISTS matches (
match_id INTEGER PRIMARY KEY AUTOINCREMENT,
home_id INTEGER NOT NULL,
away_id INTEGER NOT NULL,
competition_id INTEGER NOT NULL,
status INTEGER default 0,
kickoff_at TIMESTAMP DEFAULT NULL,
tz TEXT NOT NULL,
venue TEXT NOT NULL,
description TEXT default NULL,
channel_name TEXT default NULL,
channel_id TEXT default NULL,
channel_topic TEXT default NULL,
is_warned BOOLEAN default FALSE,
welcome_msg_id TEXT default NULL,
hours_before_kickoff INTEGER default NULL,
hours_after_kickoff INTEGER default NULL,
watch TEXT default NULL,
streams TEXT default NULL,
created_by TEXT default NULL,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
lastmodified_by TEXT default NULL,
lastmodified_at timestamp default NULL
);

CREATE TABLE IF NOT EXISTS info (
 info_id INTEGER PRIMARY KEY AUTOINCREMENT,
 obj TEXT NOT NULL,
 field TEXT NOT NULL,
 info TEXT DEFAULT NULL
 );

CREATE TABLE IF NOT EXISTS managers (
user_id TEXT NOT NULL PRIMARY KEY,
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
created_by TEXT DEFAULT NULL,
`level` INTEGER default 99
);

CREATE TABLE IF NOT EXISTS manager_competitions (
user_id TEXT NOT NULL,
competition_id INTEGER NOT NULL,
PRIMARY KEY(user_id, competition_id)
);

CREATE TABLE IF NOT EXISTS config (field TEXT PRIMARY KEY NOT NULL, value TEXT);

CREATE TABLE IF NOT EXISTS bot_statuses (
 status_id INTEGER PRIMARY KEY AUTOINCREMENT,
 status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS canuckbot_cache (
 key TEXT PRIMARY KEY,
 data TEXT,
 timestamp INTEGER,
 expiration INTEGER
);
